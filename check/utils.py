import datetime
import enum
from uuid import UUID

from auth.schemas import JWTUser


def check_user(user: JWTUser, **kwargs) -> bool:
    if user.role == "client":
        return user.data.get("clientId") == kwargs.get("clientId")

    if user.role == "worker":
        return user.data.get("clientId") == kwargs.get("clientId") and user.data.get(
            "organizationId"
        ) == kwargs.get("organizationId")

    return False

def change_format(body: dict) -> dict:
    result = {}
    naming_map = {
        "id": "id",
        "cashRegisterCheckNumber": "number",
        "number": "cashRegisterCheckNumber",
        "fiscalDocumentNumber": "number_fiscal_document",
        "number_fiscal_document": "fiscalDocumentNumber",
        "sum": "amount",
        "amount": "sum",
        "date": "date",
        
        "client_id": "clientId",
        "clientId": "client_id",
        
        "cash_shift_id": "checkoutShiftId",
        "checkoutShiftId": "cash_shift_id",
        
        "check_status": "status",
        "status": "check_status",
        
        "type_payment": "typePayment",
        "typePayment": "type_payment",
        
        "type_operation": "typeOperation",
        "typeOperation": "type_operation",
        
        "type_taxation": "taxSystem",
        "taxSystem": "type_taxation",
        
        "positions": "positions",
    }
    for name in naming_map.keys():
        if name in body:
            if isinstance(body[name], UUID):
                result[naming_map[name]] = str(body[name])
            elif isinstance(body[name], datetime.datetime):
                result[naming_map[name]] = datetime.datetime.strftime(body[name], "%Y-%m-%dT%H:%M:%S")
            else:
                result[naming_map[name]] = body[name]
    return result

class TypesPayment(enum.Enum):
    CASH = "cash"
    CASHLESS = 'cashless'
    
class CheckStatuses(enum.Enum):
    CREATED = 'created'
    CLOSED = 'closed'
    RETURNED = "returned"


    





