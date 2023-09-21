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
    workplaceId: str = None,
    workerId: str = None,
    closed: bool = None,
    hidden: bool = None,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/getCheckoutShifts"]
    ),
):
    if not check_user(
        user, clientId=clientId, organizationId=organizationId, workerId=workerId
    ):
        raise PermissionDenied

    filter_by = {
        "client_id": uuid.UUID(clientId),
        "organization_id": uuid.UUID(organizationId),
    }

    if workplaceId is not None:
        filter_by["workplace_id"] = uuid.UUID(workplaceId)
    if workerId is not None:
        filter_by["worker_id"] = uuid.UUID(workerId)
    if closed is not None:
        filter_by["closed"] = closed
    if hidden is not None:
        filter_by["hide"] = hidden

    checkout_shifts = await CheckoutShiftDAO.json_get_all(filter_by)

    return JSONResponse(content=checkout_shifts, status_code=200)


@router.get("/getCheckoutShift")
async def get_checkout_shift(
    clientId: str,
    organizationId: str,
    checkoutShiftId: str,
    workerId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/getCheckoutShift"]
    ),
):
    if not check_user(
        user, clientId=clientId, organizationId=organizationId, workerId=workerId
    ):
        raise PermissionDenied

    checkout_shift = await CheckoutShiftDAO.json_find_one(
        id=uuid.UUID(checkoutShiftId),
        filter_by={
            "organization_id": uuid.UUID(organizationId),
            "client_id": uuid.UUID(clientId),
            "worker_id": uuid.UUID(workerId),
        },
    )
    if checkout_shift is not None:
        return JSONResponse(content=checkout_shift, status_code=200)
    else:
        raise NotFound


@router.post("/openCheckoutShift")
async def open_checkout_shift(
    clientId: str,
    organizationId: str,
    workerId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/openCheckoutShift"]
    ),
    **body: dict,
):
    if not check_user(
        user, clientId=clientId, organizationId=organizationId, workerId=workerId
    ):
        raise PermissionDenied

    checkout_shift = await CheckoutShiftDAO.json_add(
        {
            **change_format(**body),
            "client_id": uuid.UUID(clientId),
            "organization_id": uuid.UUID(organizationId),
            "worker_id": uuid.UUID(workerId),
            "date": datetime.datetime.utcnow(),
        }
    )

    return JSONResponse(content=checkout_shift, status_code=200)


@router.patch("/closeCheckoutShift")
async def close_checkout_shift(
    clientId: str,
    organizationId: str,
    workerId: str,
    checkoutShiftId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/closeCheckoutShift"]
    ),
):
    if not check_user(
        user, clientId=clientId, organizationId=organizationId, workerId=workerId
    ):
        raise PermissionDenied

    checkout_shift = await CheckoutShiftDAO.json_update(
        id=uuid.UUID(checkoutShiftId),
        filter_by={
            "client_id": uuid.UUID(clientId),
            "organization_id": uuid.UUID(organizationId),
            "worker_id": uuid.UUID(workerId),
        },
        data={"closed": True},
    )

    if checkout_shift is not None:
        return JSONResponse(content=checkout_shift, status_code=200)
    else:
        raise NotFound
