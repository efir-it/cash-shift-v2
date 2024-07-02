from dataclasses import dataclass
import enum
import json
from typing import Annotated, Optional
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_serializer

from check.schemas import ReceiptResponse, ReceiptWithPositionsResponse


class BaseCashShift(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_serializer(
        "id",
        "owner_id",
        "worker_id",
        "organization_id",
        "store_id",
        "workplace_id",
        "cash_registr_id",
        check_fields=False,
    )
    def uuid_to_str(uuid: uuid.UUID | None):
        return str(uuid) if uuid else None

    @field_serializer("date", check_fields=False)
    def datetime_to_str(date: datetime):
        return datetime.strftime(date, "%Y-%m-%dT%H:%M:%S")
    
    @field_serializer("closed_date", check_fields=False)
    def datetime_to_str_close(closed_date: datetime | None):
        return datetime.strftime(closed_date, "%Y-%m-%dT%H:%M:%S") if closed_date else None


class CashShiftResponse(BaseCashShift):
    id: uuid.UUID
    number: Optional[int]
    date: datetime
    closed_date: Optional[datetime] = Field(alias="closedDate", default=None)
    organization_id: uuid.UUID = Field(alias="organizationId")
    owner_id: uuid.UUID = Field(alias="ownerId")
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
    worker_id: uuid.UUID | None = Field(alias="workerId", default=None)
    cash_registr_id: uuid.UUID | None = Field(alias="cashRegistrId", default=None)
    closed: bool
    hide: bool = Field(alias="hidden")


class CashShiftWithReceiptsResponse(CashShiftResponse):
    receipts: list[ReceiptWithPositionsResponse] = Field(alias="cashReceipts")


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
    worker_id: uuid.UUID | None = Field(alias="workerId", default=None)
    id: uuid.UUID = Field(alias="checkoutShiftId")


class CashShiftUserLastRequest(BaseRequest):
    worker_id: uuid.UUID | None = Field(alias="workerId", default=None)
    
class CashShiftWorkplaceLastRequest(BaseRequest):
    workplace_id: uuid.UUID = Field(alias="workplaceId")


class CashShiftOpenRequest(BaseRequest):
    worker_id: uuid.UUID | None = Field(alias="workerId", default=None)


class CashShiftOpenRequestBody(BaseCashShift):
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
    number: int | None = Field(default=None)
    cash_registr_id: uuid.UUID | None = Field(alias="cashRegistrId", default=None)


class CashShiftClosedResponse(BaseCashShift):
    id: uuid.UUID
    number: Optional[int]
    date: datetime
    closed_date: datetime = Field(alias="closedDate")
    organization_id: uuid.UUID = Field(alias="organizationId")
    owner_id: uuid.UUID = Field(alias="ownerId")
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
    worker_id: uuid.UUID | None = Field(alias="workerId", default=None)
    cash_registr_id: uuid.UUID | None = Field(alias="cashRegistrId", default=None)
    closed: bool
    hide: bool = Field(alias="hidden")


class CashShiftClosedWithReceiptsResponse(CashShiftClosedResponse):
    receipts: list[ReceiptWithPositionsResponse] = Field(alias="cashReceipts")
