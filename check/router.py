import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from check.dao import CheckDAO
from check.schemas import CheckSchema
from event.producers import SaleCheckProducer, ReturnCheckProducer

router = APIRouter(prefix="/checkoutShift", tags=["Чеки"])


@router.get("/getCashReceipt")
async def get_check(clientID: str, cashReceiptID: str):
    check = await CheckDAO.json_get_all(**{"id": int(cashReceiptID)})
    return JSONResponse(content=check, status_code=200)


@router.post("/createCashReceipt")
async def add_check(clientID: str, checkOutShiftID: str, body):
    data = {
        "client_id": int(clientID),
        "date": datetime.datetime.utcnow(),
        "number": body["cashRegisterCheckNumber"],
        "amount": body["sum"],
        "number_fiscal_document": body["fiscalDocumentNumber"],
        "cash_shift_id": int(checkOutShiftID),
        "type_operation_id": body["typeID"],
        "type_payment_id": body["cashID"],
        "check_status_id": body["statusID"],
        "type_taxation_id": body["taxSystemID"],
        "positions": body["positions"],
    }
    check = await CheckDAO.json_add(**data)
    return JSONResponse(content=check, status_code=200)


@router.patch("/returnCashReceipt")
async def return_check(clientID: str, cashReceiptID: str):
    check = await CheckDAO.json_update(
        id=int(cashReceiptID), data={"check_status_id": 3}
    )
    producer = ReturnCheckProducer()
    await producer.send_messages(
        {
            "cashReceiptId": check["id"],
            "storeId": 1,
            "clientId": 1,
            "organizationId": 1,
            "createTime": check["date"],
            "workerId": 1,
            "positions": check["positions"],
        }
    )
    producer.connection_close()
    return JSONResponse(content=check, status_code=200)


@router.patch("/closeCashReceipt")
async def close_check(clientID: str, cashReceiptID: str):
    check = await CheckDAO.json_update(
        id=int(cashReceiptID), data={"check_status_id": 2}
    )
    producer = SaleCheckProducer()
    await producer.send_messages(
        {
            "cashReceiptId": check["id"],
            "storeId": 1,
            "clientId": 1,
            "organizationId": 1,
            "createTime": check["date"],
            "workerId": 1,
            "positions": check["positions"],
        }
    )
    producer.connection_close()
    return JSONResponse(content=check, status_code=200)


@router.delete("/removeCashReceipt")
async def remove_check(clientID: str, cashReceiptID: str):
    check = await CheckDAO.json_remove(int(cashReceiptID))
    return JSONResponse(content=check, status_code=200)
