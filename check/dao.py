import datetime
from check.models import Check
from dao.base import BaseDAO

from check_status.dao import CheckStatusDAO
from type_operation.dao import TypeOperationDAO
from type_payment.dao import TypePaymentDAO
from type_taxation.dao import TypeTaxationDAO
from position_check.dao import PositionCheckDAO


class CheckDAO(BaseDAO):
    model = Check

    @classmethod
    async def json_find_by_id(cls, id) -> dict:
        check = await cls.find_by_id(id)
        return {
            "id": check.id,
            "checkoutShiftID": check.cash_shift_id,
            "type": await TypeOperationDAO.json_find_by_id(id=check.type_operation_id),
            "date": datetime.datetime.strftime(check.date, "%Y-%m-%dT%H:%M:%S"),
            "sum": check.amount,
            "cash": await TypePaymentDAO.json_find_by_id(id=check.type_payment_id),
            "cashRegisterCheckNumber": check.number,
            "fiscalDocumentNumber": check.number_fiscal_document,
            "taxSystem": await TypeTaxationDAO.json_find_by_id(
                id=check.type_taxation_id
            ),
            "status": await CheckStatusDAO.json_find_by_id(id=check.check_status_id),
            "positions": await PositionCheckDAO.json_get_all(**{"check_id": check.id}),
        }

    @classmethod
    async def json_get_all(cls, **filter_by) -> dict:
        checks = await cls.get_all(**filter_by)
        return [
            {
                "id": check.id,
                "type": await TypeOperationDAO.json_find_by_id(
                    id=check.type_operation_id
                ),
                "date": datetime.datetime.strftime(check.date, "%Y-%m-%dT%H:%M:%S"),
                "sum": check.amount,
                "cash": await TypePaymentDAO.json_find_by_id(id=check.type_payment_id),
                "cashRegisterCheckNumber": check.number,
                "fiscalDocumentNumber": check.number_fiscal_document,
                "taxSystem": await TypeTaxationDAO.json_find_by_id(
                    id=check.type_taxation_id
                ),
                "status": await CheckStatusDAO.json_find_by_id(
                    id=check.check_status_id
                ),
                "positions": await PositionCheckDAO.json_get_all(
                    **{"check_id": check.id}
                ),
            }
            for check in checks
        ]

    @classmethod
    async def json_add(cls, **data) -> dict:
        positions_check = data.pop("positions")
        check = await cls.add(**data)
        for position, position_check in enumerate(positions_check):
            await PositionCheckDAO.add(
                **{
                    "product_id": position_check["productID"],
                    "count": position_check["count"],
                    "price": position_check["price"],
                    "client_id": check.client_id,
                    "check_id": check.id,
                    "position": position + 1,
                }
            )
        return {
            "id": check.id,
            "checkoutShiftID": check.cash_shift_id,
            "type": await TypeOperationDAO.json_find_by_id(id=check.type_operation_id),
            "date": datetime.datetime.strftime(check.date, "%Y-%m-%dT%H:%M:%S"),
            "sum": check.amount,
            "cash": await TypePaymentDAO.json_find_by_id(id=check.type_payment_id),
            "cashRegisterCheckNumber": check.number,
            "fiscalDocumentNumber": check.number_fiscal_document,
            "taxSystem": await TypeTaxationDAO.json_find_by_id(
                id=check.type_taxation_id
            ),
            "status": await CheckStatusDAO.json_find_by_id(id=check.check_status_id),
            "positions": await PositionCheckDAO.json_get_all({"check_id": check.id}),
        }

    @classmethod
    async def json_remove(cls, id) -> dict:
        positions = await PositionCheckDAO.json_get_all(**{"check_id": id})
        check = await cls.delete(id)
        return {
            "id": check.id,
            "checkoutShiftID": check.cash_shift_id,
            "type": await TypeOperationDAO.json_find_by_id(id=check.type_operation_id),
            "date": datetime.datetime.strftime(check.date, "%Y-%m-%dT%H:%M:%S"),
            "sum": check.amount,
            "cash": await TypePaymentDAO.json_find_by_id(id=check.type_payment_id),
            "cashRegisterCheckNumber": check.number,
            "fiscalDocumentNumber": check.number_fiscal_document,
            "taxSystem": await TypeTaxationDAO.json_find_by_id(
                id=check.type_taxation_id
            ),
            "status": await CheckStatusDAO.json_find_by_id(id=check.check_status_id),
            "positions": positions,
        }

    @classmethod
    async def json_update(cls, id, **data) -> dict:
        check = await cls.update(id, **data)
        return {
            "id": check.id,
            "checkoutShiftID": check.cash_shift_id,
            "type": await TypeOperationDAO.json_find_by_id(id=check.type_operation_id),
            "date": datetime.datetime.strftime(check.date, "%Y-%m-%dT%H:%M:%S"),
            "sum": check.amount,
            "cash": await TypePaymentDAO.json_find_by_id(id=check.type_payment_id),
            "cashRegisterCheckNumber": check.number,
            "fiscalDocumentNumber": check.number_fiscal_document,
            "taxSystem": await TypeTaxationDAO.json_find_by_id(
                id=check.type_taxation_id
            ),
            "status": await CheckStatusDAO.json_find_by_id(id=check.check_status_id),
            "positions": await PositionCheckDAO.json_get_all(**{"check_id": check.id}),
        }
