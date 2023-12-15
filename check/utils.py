import datetime
import enum
from typing import Callable
from uuid import UUID

from auth.schemas import JWTUser

dict_without_none_values: Callable[[dict], dict] = lambda dict: {
    k: v for k, v in dict.items() if v is not None
}


def check_user(user: JWTUser, **kwargs) -> bool:
    print(user)
    check_fields = ["ownerId", "organizationId", "workerId"]
    if user.role == "owner":
        return str(user.data.get("ownerId")) == str(kwargs.get("ownerId"))

    if user.role == "worker":
        for field in check_fields:
            field_from_request = kwargs.get(field, None)
            if field_from_request is not None and str(user.data.get(field)) != str(
                field_from_request
            ):
                return False

    return True


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
        "owner_id": "ownerId",
        "ownerId": "owner_id",
        "store_id": "storeId",
        "storeId": "store_id",
        "reason_id": "reasonId",
        "reasonId": "reason_id",
        "worker_id": "workerId",
        "workerId": "worker_id",
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
        "timeStart": "time_start",
        "timeEnd": "time_end",
        "count": "count",
    }
    for name in naming_map.keys():
        if name in body:
            if isinstance(body[name], UUID):
                result[naming_map[name]] = str(body[name])
            elif isinstance(body[name], datetime.datetime):
                result[naming_map[name]] = datetime.datetime.strftime(
                    body[name], "%Y-%m-%dT%H:%M:%S"
                )
            else:
                result[naming_map[name]] = body[name]
    return result
