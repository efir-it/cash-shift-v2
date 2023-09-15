import datetime
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
        "date": "openedTime",
        "openedTime": "date",
        "organization_id": "organizationId",
        "organizationId": "organization_id",
        "store_id": "storeId",
        "storeId": "store_id",
        "client_id": "clientId",
        "clientId": "client_id",
        "workplace_id": "workplaceId",
        "workplaceId": "workplace_id",
        "personal_id": "personalId",
        "personalId": "personal_id",
        "cash_registr_id": "cashRegistrId",
        "cashRegistrId": "cash_registr_id",
        "closed": "closed",
        "hide": "hidden",
        "hidden": "hide",
        "checks": "cashReceipts",
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


    





