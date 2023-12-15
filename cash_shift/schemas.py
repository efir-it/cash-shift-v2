import enum
import json
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from check.schemas import ReceiptResponse, ReceiptWithPositionsResponse


class BaseCashShift(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_serializer(
        "id",
        "worker_id",
        "owner_id",
        "organization_id",
        "store_id",
        "workplace_id",
        "cash_registr_id",
        check_fields=False,
    )
    def uuid_to_str(uuid: uuid.UUID):
        return str(uuid) if uuid else None

    @field_serializer("date", check_fields=False)
    def datetime_to_str(date: datetime):
        return datetime.strftime(date, "%Y-%m-%dT%H:%M:%S")


class CashShiftResponse(BaseCashShift):
    id: uuid.UUID
    date: datetime
    organization_id: uuid.UUID = Field(alias="organizationId")
    owner_id: uuid.UUID = Field(alias="ownerId")
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
    worker_id: uuid.UUID = Field(alias="workerId")
    cash_registr_id: uuid.UUID = Field(alias="cashRegistrId")
    closed: bool
    hide: bool = Field(alias="hidden")


class CashShiftWithReceiptsResponse(CashShiftResponse):
    receipts: list[ReceiptResponse] = Field(alias="cashReceipts")


class CashShiftsResponse(BaseCashShift):
    cash_shifts: list[CashShiftResponse] = Field(alias="checkoutShifts")


class BaseRequest(BaseCashShift):
    owner_id: uuid.UUID = Field(alias="ownerId")
    organization_id: uuid.UUID = Field(alias="organizationId")


class CashShiftsRequest(BaseRequest):
    worker_id: uuid.UUID | None = Field(default=None, alias="workerId")
    workplace_id: uuid.UUID | None = Field(default=None, alias="workplaceId")
    closed: bool | None = Field(default=None)
    hide: bool | None = Field(default=None, alias="hidden")


class CashShiftRequest(BaseRequest):
    worker_id: uuid.UUID = Field(alias="workerId")
    id: uuid.UUID = Field(alias="checkoutShiftId")


class CashShiftLastRequest(BaseRequest):
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")


class CashShiftOpenRequest(BaseRequest):
    worker_id: uuid.UUID = Field(alias="workerId")


class CashShiftOpenRequestBody(BaseCashShift):
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
    cash_registr_id: uuid.UUID = Field(alias="cashRegistrId")
