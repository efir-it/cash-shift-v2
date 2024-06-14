import datetime
import uuid
from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from exceptions import PermissionDenied, ReceiptNotFound
from position_check.dao import PositionCheckDAO
from position_check.schemas import PositionsChecksResponse

router = APIRouter(prefix="/positionCheck", tags=["Позиции чека"])


@router.post("/getPositions", response_model=List[PositionsChecksResponse])
async def get_positions(
    body: List[uuid.UUID],
) -> List[PositionsChecksResponse]:
    positions: List[PositionsChecksResponse] = await PositionCheckDAO.get_all_positions_by_ids(body)

    if positions is None:
        positions = []
    return positions
    # if positions:
    #     return JSONResponse(content=[position.model_dump(by_alias=True, exclude_unset=True) for position in positions], status_code=200)
    # else:
    #     raise ReceiptNotFound



















# @router.get("/getCashReceipts")
# async def get_checks(
#     params: ReceiptsRequest = Depends(),
# ) -> ReceiptWithPositionsResponse:
#     receipts: list[ReceiptWithPositionsResponse] = await CheckDAO.get_all_receipts(
#         params.model_dump(exclude_none=True)
#     )
#
#     return JSONResponse(
#         content=ReceiptsResponse(receipts=receipts).model_dump(by_alias=True),
#         status_code=200,
#     )
#
#
# @router.get("/getCashReceipt")
# async def get_check(params: ReceiptRequest = Depends()) -> ReceiptWithPositionsResponse:
#     receipt: ReceiptWithPositionsResponse | None = await CheckDAO.get_one_receipt(
#         params.model_dump(exclude_none=True)
#     )
#
#     if receipt is not None:
#         return JSONResponse(content=receipt.model_dump(by_alias=True), status_code=200)
#     else:
#         raise ReceiptNotFound
