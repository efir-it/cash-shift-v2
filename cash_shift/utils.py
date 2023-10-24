import datetime
from uuid import UUID

from auth.schemas import JWTUser


def check_user(user: JWTUser, **kwargs) -> bool:
    check_fields = ["ownerId", "organizationId", "workerId"]
    if user.role == "owner":
        return user.data.get("ownerId") == kwargs.get("ownerId")

    if user.role == "worker":
        for field in check_fields:
            field_from_request = kwargs.get(field, None)
            if (
                field_from_request is not None
                and user.data.get(field) != field_from_request
            ):
                return False

    return True


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
        "owner_id": "ownerId",
        "ownerId": "owner_id",
        "workplace_id": "workplaceId",
        "workplaceId": "workplace_id",
        "worker_id": "workerId",
        "workerId": "worker_id",
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
                result[naming_map[name]] = datetime.datetime.strftime(
                    body[name], "%Y-%m-%dT%H:%M:%S"
                )
            else:
                result[naming_map[name]] = body[name]
    return result
