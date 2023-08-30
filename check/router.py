import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from check.dao import CheckDAO
from check.schemas import CheckSchema
from type_operation.dao import TypeOperationDAO
from type_payment.dao import TypePaymentDAO
from type_taxation.dao import TypeTaxationDAO
from check_status.dao import CheckStatusDAO
from cash_shift.dao import CashShiftDAO
from position_check.dao import PositionCheckDAO
from event.producers import SaleCheckProducer, ReturnCheckProducer

router = APIRouter(prefix="/checkoutShift", tags=["Чеки"])


@router.get("")
async def get_checks() -> list[CheckSchema]:
    return await CheckDAO.get_all()


@router.get("/{id}")
async def get_check(id: int) -> CheckSchema:
    return await CheckDAO.find_by_id(id)


@router.post("")
async def add_check(item: dict):
    format = "%Y-%m-%dT%H:%M:%S"
    if "date" in item:
        item["date"] = datetime.datetime.strptime(item["date"], format)
    return await CheckDAO.add(**item)


@router.put("/{id}")
async def update_check(id: int, **data: dict):
    return await CheckDAO.update(id, **data)


@router.delete("/{id}")
async def delete_check(id: int):
    return await CheckDAO.delete(id)

@router.patch("/returnCashReceipt")
async def return_check(clientId: str, cashReceiptID: str):
    check = await CheckDAO.update(
        id=int(cashReceiptID), 
        data={
            "check_status_id": 3,
        }
    )
    type_operation = await TypeOperationDAO.find_by_id(check.type_operation_id)
    print(type(type_operation), type_operation)
    type_payment = await TypePaymentDAO.find_by_id(check.type_payment_id)
    type_taxation = await TypeTaxationDAO.find_by_id(check.type_taxation_id)
    check_status = await CheckStatusDAO.find_by_id(check.check_status_id)
    cash_shift = await CashShiftDAO.find_by_id(check.cash_shift_id)
    
    response_body = {
        "id": check.id,
        "checkoutShiftID": check.cash_shift_id,
        "type": {
            "id": type_operation.id,
            "name": type_operation.name,
        },  
        "date": check.date,
        "sum": check.amount,
        "cash":{
            "id": type_payment.id,
            "name": type_payment.name
        },
        "cashRegisterCheckNumber": check.number,
        "fiscalDocumentNumber": check.number_fiscal_document,
        "taxSystem": {
            "id": type_taxation.id,
            "name": type_taxation.name,
        },
        "stateName": check_status.name,
        "positions": [
            {
                "id": position.id,
                "product": position.product_id,
                "count": position.count,
                "price": position.price,
            } for position in check.positions
        ]
    }
    
    producer = ReturnCheckProducer()
    producer.send_messages(
        {
            "cashReceiptId": check.id,
            "storeId": cash_shift.store_id,
            "clientId": check.client_id,
            "organizationId": cash_shift.organization_id,
            "createTime": check.date,
            "workerId": cash_shift.worker_id
        }
    )
    producer.connection_close()
    return JSONResponse(content=response_body, status_code=200)

@router.post("/createCashReceipt")
async def add_check(clientID: str, checkOutShiftID: str, data):
    pass

@router.patch("/closeCashReceipt")
async def close_check(clientID: str, cashReceiptID: str):
    check = await CheckDAO.update(
        id=int(cashReceiptID),
        data={
            "check_status_id": 2
        }
    )
    type_operation = await TypeOperationDAO.find_by_id(check.type_operation_id)
    type_payment = await TypePaymentDAO.find_by_id(check.type_payment_id)
    type_taxation = await TypeTaxationDAO.find_by_id(check.type_taxation_id)
    check_status = await CheckStatusDAO.find_by_id(check.check_status_id)
    cash_shift = await CashShiftDAO.find_by_id(check.cash_shift_id)
    positions = await PositionCheckDAO.get_all(
        **{
            "check_id": check.id
        }
    )
    response_body = {
        "id": check.id,
        "checkoutShiftID": check.cash_shift_id,
        "type": {
            "id": type_operation.id,
            "name": type_operation.name,
        },  
        "date": datetime.datetime.strftime(check.date, "%Y-%m-%dT%H:%M:%S"),
        "sum": check.amount,
        "cash":{
            "id": type_payment.id,
            "name": type_payment.name
        },
        "cashRegisterCheckNumber": check.number,
        "fiscalDocumentNumber": check.number_fiscal_document,
        "taxSystem": {
            "id": type_taxation.id,
            "name": type_taxation.name,
        },
        "stateName": check_status.name,
        "positions": [
            {
                "id": position.id,
                "product": position.product_id,
                "count": position.count,
                "price": position.price,
            } for position in positions
        ]
    }
    
    producer = SaleCheckProducer()
    await producer.send_messages(
        {
            "cashReceiptId": check.id,
            "storeId": 1,
            "clientId": check.client_id,
            "organizationId": cash_shift.organization_id,
            "createTime": datetime.datetime.strftime(check.date, "%Y-%m-%dT%H:%M:%S"),
            "workerId": cash_shift.worker_id
        }
    )
    producer.connection_close
    return JSONResponse(
        content=response_body,
        status_code=200
    )
    