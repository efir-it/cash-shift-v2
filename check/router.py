import datetime
import uuid
from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from auth.dependencies import get_current_user
from auth.schemas import JWTUser

from check.dao import CheckDAO
from check.schemas import CheckSchema
from check.utils import CheckStatuses, change_format, check_user
from event.producers import SaleCheckProducer, ReturnCheckProducer
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
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied
    
    check = await CheckDAO.json_find_by_id(uuid.UUID(cashReceiptId))
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
    **body: dict
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied
    
    data = change_format(**body)
    data["client_id"] = uuid.UUID(clientId)
    data["cash_shift_id"] = uuid.UUID(checkoutShiftId)
    data["check_status"] = CheckStatuses.CREATED.value
    data["date"] = datetime.datetime.utcnow()
    check = await CheckDAO.json_add(**data)
    if check:
        return JSONResponse(content=check, status_code=200)
    else:
        raise NotFound


@router.patch("/returnCashReceipt")
async def return_check(
    clientId: str,
    organizationId: str,
    cashReceiptId: str,
    user: JWTUser = Security(
        get_current_user, scopes=["/checkoutShift/returnCashReceipt"]
    ),
):
    if not check_user(user, clientId=clientId, organizationId=organizationId):
        raise PermissionDenied
    
    check = await CheckDAO.json_update(
        uuid.UUID(cashReceiptId), **{"check_status": CheckStatuses.RETURNED.value}
    )
    if check:
        producer = ReturnCheckProducer()
        await producer.send_messages(
            {
                "cashReceiptId": check["id"],
                "storeId": "384299e4-86ea-460a-978e-170f6aafad8f",
                "clientId": clientId,
                "organizationId": organizationId,
                "createTime": check["date"],
                "workerId": user.data.get("workerId", None),
                "positions": check["positions"],
            }
        )
        producer.connection_close()
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
        uuid.UUID(cashReceiptId), **{"check_status": CheckStatuses.CLOSED.value}
    )
    
    if check:
        producer = SaleCheckProducer()
        await producer.send_messages(
            {
                "cashReceiptId": check["id"],
                "storeId": "384299e4-86ea-460a-978e-170f6aafad8f",
                "clientId": clientId,
                "organizationId": organizationId,
                "createTime": check["date"],
                "workerId":  user.data.get("workerId", None),
                "positions": check["positions"],
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
    
    check = await CheckDAO.json_remove(uuid.UUID(cashReceiptId))
    if check:
        return JSONResponse(content=check, status_code=200)
    else:
        raise NotFound
