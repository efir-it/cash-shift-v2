from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class PositionCheckSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    count: int
    price: int
    position: int
    owner_id: uuid.UUID
    check_id: uuid.UUID
    price_may_change_in_cash_receipt: bool = Field(alias="PriceMayChangeInCashReceipt")
    price_min_in_cash_receipt: int = Field(alias="PriceMinInCashReceipt")
    price_max_in_cash_receipt: int = Field(alias="PriceMaxInCashReceipt")


class BasePosition(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_serializer("id", "product_id", "owner_id", "check_id", check_fields=False)
    def uuid_to_str(uuid: uuid.UUID):
        return str(uuid) if uuid else None


class PositionResponse(BasePosition):
    id: uuid.UUID
    # check_id: uuid.UUID
    product_id: uuid.UUID = Field(alias="productId")
    count: int
    price: int
    position: int


class PositionCreateRequest(BasePosition):
    product_id: uuid.UUID = Field(alias="productId")
    count: int
    price: int


class Check(BaseModel):
    id: uuid.UUID


class PositionsChecksResponse(BasePosition):
    id: uuid.UUID
    product_id: uuid.UUID
    count: int
    price: int
    position: int
    owner_id: uuid.UUID
    check_id: uuid.UUID
    price_may_change_in_cash_receipt: bool
    price_min_in_cash_receipt: Optional[int]
    price_max_in_cash_receipt: Optional[int]


