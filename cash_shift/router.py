import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from cash_shift.dao import CheckoutShiftDAO
from cash_shift.schemas import CashShiftSchemas

router = APIRouter(prefix="/checkoutShift", tags=["Кассовые смены"])


@router.get("/getCheckoutShiftList")
async def get_checkout_shift_list(
    clientID: str,
    organizationID: str,
    passClosed: bool,
    workplaceID: str = None,
    cashRegistrID: str = None,
    passHidden: bool = False,
):
    filter_by = {
        "client_id": int(clientID),
        "organization_id": int(organizationID),
        "status": not passClosed,
        "hide": passHidden,
    }
    if workplaceID is not None:
        filter_by["workplace_id"] = int(workplaceID)
    if cashRegistrID is not None:
        filter_by["cash_registr_id"] = int(cashRegistrID)

    checkout_shifts = await CheckoutShiftDAO.json_get_all(**filter_by)
    return JSONResponse(content=checkout_shifts, status_code=200)


@router.get("/getCheckoutShift")
async def get_checkout_shift(clientID: str, checkoutShiftID: str):
    checkout_shifts = await CheckoutShiftDAO.json_find_by_id(int(checkoutShiftID))
    return JSONResponse(content=checkout_shifts, status_code=200)


@router.post("/openCheckoutShift")
async def open_checkout_shift(clientID: str, workplaceID: str, **body: dict):
    body = body["body"]
    data = {
        "client_id": int(clientID),
        "workplace_id": int(workplaceID),
        "store_id": body["storeID"],
        "organization_id": body["organizationID"],
        "personal_id": body["personalID"],
        "cash_registr_id": body["cashRegistrID"],
        "status": True,
        "hide": False,
        "date": datetime.datetime.utcnow(),
    }
    checkout_shift = await CheckoutShiftDAO.json_add(**data)
    return JSONResponse(content=checkout_shift, status_code=200)


@router.patch("/closeCheckoutShift")
async def close_checkout_shift(clientID: str, checkoutShiftID: str):
    checkout_shift = await CheckoutShiftDAO.json_update(
        id=int(checkoutShiftID), data={"status": False}
    )
    return JSONResponse(content=checkout_shift, status_code=200)
