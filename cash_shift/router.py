from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from cash_shift.dao import CheckoutShiftDAO
from cash_shift.schemas import (
    CashShiftLastRequest,
    CashShiftOpenRequest,
    CashShiftOpenRequestBody,
    CashShiftRequest,
    CashShiftResponse,
    CashShiftsRequest,
    CashShiftsResponse,
    CashShiftWithReceiptsResponse,
)
from exceptions import CheckoutShiftNotFound

router = APIRouter(prefix="/checkoutShift", tags=["Кассовые смены"])


@router.get("/getCheckoutShifts")
async def get_checkout_shift_list(
    params: CashShiftsRequest = Depends(),
) -> CashShiftsResponse:
    checkout_shifts: list[
        CashShiftResponse
    ] = await CheckoutShiftDAO.get_all_checkout_shifts(
        params.model_dump(exclude_none=True)
    )

    return JSONResponse(
        content=CashShiftsResponse(cash_shifts=checkout_shifts).model_dump(
            by_alias=True
        ),
        status_code=200,
    )


@router.get("/getCheckoutShift")
async def get_checkout_shift(
    params: CashShiftRequest = Depends(),
) -> CashShiftWithReceiptsResponse:
    checkout_shift: CashShiftWithReceiptsResponse | None = (
        await CheckoutShiftDAO.get_one_checkout_shift(
            params.model_dump(exclude_none=True)
        )
    )

    if checkout_shift is not None:
        return JSONResponse(
            content=checkout_shift.model_dump(by_alias=True), status_code=200
        )
    else:
        raise CheckoutShiftNotFound


@router.get("/getLastCheckoutShift")
async def get_last_checkout_shift(
    params: CashShiftLastRequest = Depends(),
) -> CashShiftWithReceiptsResponse:
    checkout_shift: CashShiftWithReceiptsResponse | None = (
        await CheckoutShiftDAO.get_last_checkout_shift(
            params.model_dump(exclude_none=True)
        )
    )

    if checkout_shift is not None:
        return JSONResponse(
            content=checkout_shift.model_dump(by_alias=True), status_code=200
        )
    else:
        raise CheckoutShiftNotFound


@router.post("/openCheckoutShift")
async def open_checkout_shift(
    body: CashShiftOpenRequestBody, params: CashShiftOpenRequest = Depends()
) -> CashShiftWithReceiptsResponse:
    checkout_shift: CashShiftWithReceiptsResponse = (
        await CheckoutShiftDAO.create_checkout_shift(
            {
                **params.model_dump(exclude_none=True),
                **body.model_dump(exclude_none=True),
            }
        )
    )

    return JSONResponse(
        content=checkout_shift.model_dump(by_alias=True), status_code=200
    )


@router.patch("/closeCheckoutShift")
async def close_checkout_shift(
    params: CashShiftRequest = Depends(),
) -> CashShiftWithReceiptsResponse:
    checkout_shift: CashShiftWithReceiptsResponse | None = (
        await CheckoutShiftDAO.update_checkout_shift(
            params.model_dump(exclude_none=True),
            {"closed": True},
        )
    )

    if checkout_shift is not None:
        return JSONResponse(
            content=checkout_shift.model_dump(by_alias=True), status_code=200
        )
    else:
        raise CheckoutShiftNotFound
