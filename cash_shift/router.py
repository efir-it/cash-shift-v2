import datetime
import uuid
from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from auth.dependencies import get_current_user
from auth.schemas import JWTUser

from cash_shift.dao import CheckoutShiftDAO
from cash_shift.schemas import CashShiftSchemas
from cash_shift.utils import change_format, check_user
from exceptions import NotFound, PermissionDenied

router = APIRouter(prefix="/checkoutShift", tags=["Кассовые смены"])


@router.get("/getCheckoutShifts")
async def get_checkout_shift_list(
    clientId: str,
    organizationId: str,
    workplaceId: str,
    closed: bool = False,
    hidden: bool = False,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/getCheckoutShifts"]
    ),
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied
    
    data = {
        "workplace_id": workplaceId,
        "closed": closed,
        "hide": hidden,
    }

    checkout_shifts = await CheckoutShiftDAO.json_get_all(**data)
    return JSONResponse(content=checkout_shifts, status_code=200)


@router.get("/getCheckoutShift")
async def get_checkout_shift(
    clientId: str,
    organizationId: str,
    checkoutShiftId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/getCheckoutShift"]
    ),
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied
    
    checkout_shift = await CheckoutShiftDAO.json_find_by_id(uuid.UUID(checkoutShiftId))
    if checkout_shift:
        return JSONResponse(content=checkout_shift, status_code=200)
    else:
        raise NotFound


@router.post("/openCheckoutShift")
async def open_checkout_shift(
    clientId: str,
    organizationId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/openCheckoutShift"]
    ),
    **body: dict
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied
    
    data = change_format(**body)
    data["client_id"] = uuid.UUID(clientId)
    data["organization_id"] = uuid.UUID(organizationId)
    data["date"] = datetime.datetime.utcnow()
    checkout_shift = await CheckoutShiftDAO.json_add(**data)
    
    return JSONResponse(content=checkout_shift, status_code=200)



@router.patch("/closeCheckoutShift")
async def close_checkout_shift(
    clientId: str,
    organizationId: str,
    checkoutShiftId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/closeCheckoutShift"]
    ),
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied
    
    checkout_shift = await CheckoutShiftDAO.json_update(
        uuid.UUID(checkoutShiftId), **{"closed": True}
    )
    
    if checkout_shift:
        return JSONResponse(content=checkout_shift, status_code=200)
    else:
        raise NotFound
