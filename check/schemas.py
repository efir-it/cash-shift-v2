import enum
import json
import uuid
from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from position_check.schemas import PositionCreateRequest, PositionResponse


class TypePayment(enum.IntEnum):
    TEST = 0
    CASH = 1
    CASHLESS = 2


class ReceiptStatus(enum.IntEnum):
    TEST = 0
    CREATED = 1
    CLOSED = 2


class TypeOperation(enum.IntEnum):
    TEST = 0
    SELL = 1
    RETURN = 2


class TypeTaxation(enum.Enum):
    TEST = 0


class BaseReceipt(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_serializer(
        "id", "store_id", "owner_id", "cash_shift_id", "reason_id", "workplace_id", "organization_id", check_fields=False
    )
    def uuid_to_str(uuid: uuid.UUID):
        return str(uuid) if uuid else None

    @field_serializer("date", check_fields=False)
    def datetime_to_str(date: datetime):
        return datetime.strftime(date, "%Y-%m-%dT%H:%M:%S")

    @field_serializer(
        "type_operation",
        "type_payment",
        "check_status",
        "type_taxation",
        check_fields=False,
    )
    def enum_to_str(type_value):
        if type(type_value) != str:
            return type_value.value

        return type_value


class ReceiptResponse(BaseReceipt):
    id: uuid.UUID
    owner_id: uuid.UUID = Field(alias="ownerId")
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
    organization_id: uuid.UUID = Field(alias="organizationId")
    cash_shift_id: uuid.UUID = Field(alias="checkoutShiftId")
    reason_id: uuid.UUID | None = Field(alias="reasonId", default=None)
    number: Optional[str] = Field(alias="cashRegisterCheckNumber", default=None)
    number_fiscal_document: Optional[str] = Field(alias="fiscalDocumentNumber", default=None)
    reasonCheckName: Optional[str] = Field(alias="reasonCheckName", default='')
    date: datetime
    amount: int = Field(alias="sum")
    type_operation: TypeOperation = Field(alias="typeOperation")
    type_payment: TypePayment = Field(alias="typePayment")
    check_status: ReceiptStatus = Field(alias="status")
    type_taxation: TypeTaxation = Field(alias="taxSystem")


class ReceiptWithPositionsResponse(ReceiptResponse):
    positions: list[PositionResponse]


class ReceiptsResponse(BaseReceipt):
    receipts: list[ReceiptResponse]


class BaseRequest(BaseReceipt):
    owner_id: uuid.UUID = Field(alias="ownerId")
    organization_id: uuid.UUID = Field(alias="organizationId")


class ReceiptRequest(BaseRequest):
    id: uuid.UUID = Field(alias="cashReceiptId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")


class ReceiptCreateRequest(BaseRequest):
    store_id: uuid.UUID = Field(alias="storeId")
    cash_shift_id: uuid.UUID = Field(alias="checkoutShiftId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")


class ReceiptUpdateRequest(BaseRequest):
    store_id: uuid.UUID = Field(alias="storeId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
    # cash_shift_id: uuid.UUID = Field(alias="checkoutShiftId")
    id: uuid.UUID = Field(alias="cashReceiptId")


class ReceiptCreateRequestBody(BaseReceipt):
    reason_id: uuid.UUID | None = Field(alias="reasonId", default=None)
    # workplace_id: uuid.UUID = Field(alias="workplaceId")
    number: str | None = Field(alias="cashRegisterCheckNumber", default=None)
    number_fiscal_document: Optional[str] | None = Field(alias="fiscalDocumentNumber", default=None)
    amount: int = Field(alias="sum")
    type_operation: TypeOperation = Field(alias="typeOperation")
    type_payment: TypePayment = Field(alias="typePayment")
    type_taxation: TypeTaxation = Field(alias="taxSystem")

    positions: list[PositionCreateRequest] = []


class ReceiptUpdateRequestBody(BaseReceipt):
    reason_id: uuid.UUID | None = Field(alias="reasonId", default=None)
    number: str | None = Field(alias="cashRegisterCheckNumber", default=None)
    number_fiscal_document: str | None = Field(alias="fiscalDocumentNumber", default=None)
    amount: int = Field(alias="sum", default=None)
    type_operation: TypeOperation = Field(alias="typeOperation", default=None)
    type_payment: TypePayment = Field(alias="typePayment", default=None)
    type_taxation: TypeTaxation = Field(alias="taxSystem", default=None)

    positions: list[PositionCreateRequest] = []


class ReceiptsRequest(BaseRequest):
    store_id: uuid.UUID | None = Field(alias="storeId", default=None)
    workplace_id: uuid.UUID | None = Field(alias="workplaceId", default=None)
    cash_shift_id: uuid.UUID | None = Field(alias="cashShiftId", default=None)
    time_start: datetime | None = Field(alias="timeStart", default=None)
    time_end: datetime | None = Field(alias="timeEnd", default=None)
    check_status: ReceiptStatus | None = Field(default=None, alias="status")
    count: int | None = Field(default=None)


class ReceiptsLastRequest(BaseRequest):
    store_id: uuid.UUID = Field(alias="storeId")
    cash_shift_id: uuid.UUID = Field(alias="cashShiftId")
    workplace_id: uuid.UUID = Field(alias="workplaceId")
