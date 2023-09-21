import datetime
import uuid

from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse

from auth.dependencies import get_current_user
from auth.schemas import JWTUser
from cash_shift.dao import CheckoutShiftDAO
from check.dao import CheckDAO
from check.utils import CheckStatuses, TypesOperations, change_format, check_user
from event.producers import ReturnCheckProducer, SaleCheckProducer
from exceptions import NotFound, PermissionDenied

router = APIRouter(prefix="/checkoutShift", tags=["Чеки"])


@router.get("/getCashReceipt")
async def get_check(
    clientId: str,
    organizationId: str,
    cashReceiptId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/getCashReceipt"]
    ),
):
    if not check_user(
        user,
        clientId=clientId,
        organizationId=organizationId,
    ):
        raise PermissionDenied

    check = await CheckDAO.json_find_one(id=uuid.UUID(cashReceiptId))
    if check:
        return JSONResponse(content=check, status_code=200)
    else:
        raise NotFound


@router.post("/createCashReceipt")
async def add_check(
    clientId: str,
    organizationId: str,
    checkoutShiftId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/createCashReceipt"]
    ),
    **body: dict,
):
    if not check_user(
        user,
        clientId=clientId,
        organizationId=organizationId,
    ):
        raise PermissionDenied

    check = await CheckDAO.json_add(
        {
            **change_format(**body),
            "client_id": uuid.UUID(clientId),
            "organization_id": uuid.UUID(organizationId),
            "cash_shift_id": uuid.UUID(checkoutShiftId),
            "check_status": CheckStatuses.CREATED.value,
            "date": datetime.datetime.utcnow(),
        }
    )
    if check:
        return JSONResponse(content=check, status_code=200)
    else:
        raise NotFound


@router.patch("/closeCashReceipt")
async def close_check(
    clientId: str,
    organizationId: str,
    cashReceiptId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/closeCashReceipt"]
    ),
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied

    check = await CheckDAO.json_update(
        id=uuid.UUID(cashReceiptId),
        filter_by={
            "client_id": uuid.UUID(clientId),
            "organization_id": uuid.UUID(organizationId),
        },
        data={"check_status": CheckStatuses.CLOSED.value},
    )

    if check is not None:
        cash_shift = await CheckoutShiftDAO.json_find_one(
            id=uuid.UUID(check["checkoutShiftId"])
        )
        producer = (
            SaleCheckProducer()
            if check["typeOperation"] == TypesOperations.SELL.value
            else None
        )
        producer = (
            ReturnCheckProducer()
            if check["typeOperation"] == TypesOperations.RETURN.value
            else producer
        )
        if producer is not None:
            await producer.send_messages(
                {
                    "cashReceiptId": check["id"],
                    "storeId": cash_shift["storeId"],
                    "clientId": clientId,
                    "organizationId": organizationId,
                    "createTime": check["date"] + "+00:00",
                    "workerId": cash_shift["workerId"],
                    "positions": [
                        {"productId": position["id"], "productCount": position["count"]}
                        for position in check["positions"]
                    ],
                }
            )
            producer.connection_close()
        return JSONResponse(content=check, status_code=200)
    else:
        raise NotFound


@router.delete("/removeCashReceipt")
async def remove_check(
    clientId: str,
    organizationId: str,
    cashReceiptId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/removeCashReceipt"]
    ),
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied

    check = await CheckDAO.json_remove(id=uuid.UUID(cashReceiptId))

    if check:
        return JSONResponse(content=check, status_code=200)
    else:
        raise NotFound
