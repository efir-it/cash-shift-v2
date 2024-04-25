import datetime
import uuid

from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse

from auth.dependencies import get_current_user
from auth.schemas import JWTUser
from cash_shift.dao import CheckoutShiftDAO
from cash_shift.schemas import CashShiftResponse, CashShiftWithReceiptsResponse
from check.dao import CheckDAO
from check.schemas import (
    ReceiptCreateRequest,
    ReceiptCreateRequestBody,
    ReceiptRequest,
    ReceiptResponse,
    ReceiptUpdateRequest,
    ReceiptsRequest,
    ReceiptsResponse,
    ReceiptStatus,
    ReceiptUpdateRequestBody,
    ReceiptWithPositionsResponse,
    TypeOperation,
)
from check.utils import change_format, check_user, dict_without_none_values
from event.producers import ReturnCheckProducer, SaleCheckProducer
from exceptions import PermissionDenied, ReceiptNotFound

router = APIRouter(prefix="/checkoutReceipt", tags=["Чеки"])


@router.get("/getCashReceipts")
async def get_checks(
    params: ReceiptsRequest = Depends(),
) -> ReceiptWithPositionsResponse:
    receipts: list[ReceiptWithPositionsResponse] = await CheckDAO.get_all_receipts(
        params.model_dump(exclude_none=True)
    )

    return JSONResponse(
        content=ReceiptsResponse(receipts=receipts).model_dump(by_alias=True),
        status_code=200,
    )


@router.get("/getCashReceipt")
async def get_check(params: ReceiptRequest = Depends()) -> ReceiptWithPositionsResponse:
    receipt: ReceiptWithPositionsResponse | None = await CheckDAO.get_one_receipt(
        params.model_dump(exclude_none=True)
    )

    if receipt is not None:
        return JSONResponse(content=receipt.model_dump(by_alias=True), status_code=200)
    else:
        raise ReceiptNotFound


@router.post("/createCashReceipt")
async def add_check(
    body: ReceiptCreateRequestBody,
    params: ReceiptCreateRequest = Depends(),
) -> ReceiptWithPositionsResponse:
    receipt: ReceiptWithPositionsResponse | None = await CheckDAO.create_receipt(
        {**params.model_dump(exclude_none=True), **body.model_dump(exclude_none=True)}
    )

    if receipt is not None:
        return JSONResponse(content=receipt.model_dump(by_alias=True), status_code=200)
    else:
        raise ReceiptNotFound


@router.patch("/updateCashReceipt")
async def update_check(
    body: ReceiptUpdateRequestBody,
    params: ReceiptUpdateRequest = Depends(),
) -> ReceiptWithPositionsResponse:
    receipt: ReceiptWithPositionsResponse | None = await CheckDAO.update_receipt(
        params.model_dump(exclude_none=True), {**body.model_dump(exclude_none=True)}
    )

    if receipt is not None:
        return JSONResponse(content=receipt.model_dump(by_alias=True), status_code=200)
    else:
        raise ReceiptNotFound


@router.patch("/closeCashReceipt")
async def close_check(
    params: ReceiptRequest = Depends(),
) -> ReceiptWithPositionsResponse:
    receipt: ReceiptWithPositionsResponse | None = await CheckDAO.close_receipt(
        params.model_dump(exclude_none=True)
    )

    if receipt is not None:
        producer = (
            SaleCheckProducer()
            if receipt.type_operation == TypeOperation.SELL
            else None
        )
        producer = (
            ReturnCheckProducer()
            if receipt.type_operation == TypeOperation.RETURN
            else producer
        )
        if producer is not None:
            checkout_shift: CashShiftWithReceiptsResponse = (
                await CheckoutShiftDAO.get_one_checkout_shift(
                    {"id": receipt.cash_shift_id}
                )
            )
            await producer.send_messages(
                {
                    "cashReceiptId": str(receipt.id),
                    "storeId": str(receipt.store_id),
                    "ownerId": str(receipt.owner_id),
                    "organizationId": str(params.organization_id),
                    "createTime": datetime.datetime.strftime(
                        receipt.date, "%Y-%m-%dT%H:%M:%S"
                    )
                    + "+00:00",
                    "workerId": str(checkout_shift.worker_id) if checkout_shift.worker_id else str(receipt.owner_id),
                    "positions": [
                        {"productId": str(position.product_id), "productCount": position.count}
                        for position in receipt.positions
                    ],
                }
            )
            producer.connection_close()

        return JSONResponse(content=receipt.model_dump(by_alias=True), status_code=200)
    else:
        raise ReceiptNotFound


@router.delete("/removeCashReceipt")
async def remove_check(
    params: ReceiptRequest = Depends(),
) -> ReceiptWithPositionsResponse:
    receipt: ReceiptWithPositionsResponse | None = await CheckDAO.remove_receipt(
        params.model_dump(exclude_none=True)
    )

    if receipt:
        return JSONResponse(content=receipt.model_dump(by_alias=True), status_code=200)
    else:
        raise ReceiptNotFound
