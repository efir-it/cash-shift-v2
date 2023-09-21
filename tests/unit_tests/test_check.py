import pytest
from fastapi.testclient import TestClient

from check.utils import CheckStatuses
from config import settings
from main import app

client = TestClient(app)


@pytest.mark.client
async def test_client_get_check_200():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == "9a4a8e01-cdb1-4556-aa3b-215297f17e2a"


@pytest.mark.client
async def test_client_get_check_401():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_get_check_403():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": "914a8e01-cdb1-4556-aa3b-215297f17e2a",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.client
async def test_client_get_check_404():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "91aa8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.worker
async def test_worker_get_check_200():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == "9a4a8e01-cdb1-4556-aa3b-215297f17e2a"


@pytest.mark.worker
async def test_worker_get_check_401():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_get_check_403():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "9a4a8e01-cdb1-4556-aa3b-215297fyq32a",
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_get_check_404():
    response = client.get(
        url="/checkoutShift/getCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9c4a8f01-cde1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.client
async def test_client_create_check_200():
    response = client.post(
        url="/checkoutShift/createCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        json={
            "sum": 12345,
            "cashRegisterCheckNumber": "21111111",
            "fiscalDocumentNumber": "111111111",
            "typeOperation": 0,
            "taxSystem": 0,
            "typePayment": 0,
            "positions": [
                {
                    "productId": "4921975f-98bd-48f9-a700-992bee0bd738",
                    "count": 1,
                    "price": 12300,
                },
                {
                    "productId": "fa049770-62be-4036-89ce-69fdbaeb8978",
                    "count": 1,
                    "price": 45,
                },
            ],
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["sum"] == 12345
    assert len(response.json()["positions"]) == 2


@pytest.mark.client
async def test_client_create_check_401():
    response = client.post(
        url="/checkoutShift/createCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        json={
            "sum": 12345,
            "cashRegisterCheckNumber": "21111111",
            "fiscalDocumentNumber": "111111111",
            "typeOperation": 0,
            "taxSystem": 0,
            "typePayment": 0,
            "positions": [
                {
                    "productId": "4921975f-98bd-48f9-a700-992bee0bd738",
                    "count": 1,
                    "price": 12300,
                },
                {
                    "productId": "fa049770-62be-4036-89ce-69fdbaeb8978",
                    "count": 1,
                    "price": 45,
                },
            ],
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_create_check_403():
    response = client.post(
        url="/checkoutShift/createCashReceipt",
        params={
            "clientId": "914a8e01-cdb1-4556-aa3b-215297f17e2a",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        json={
            "sum": 12345,
            "cashRegisterCheckNumber": "21111111",
            "fiscalDocumentNumber": "111111111",
            "typeOperation": 0,
            "taxSystem": 0,
            "typePayment": 0,
            "positions": [
                {
                    "productId": "4921975f-98bd-48f9-a700-992bee0bd738",
                    "count": 1,
                    "price": 12300,
                },
                {
                    "productId": "fa049770-62be-4036-89ce-69fdbaeb8978",
                    "count": 1,
                    "price": 45,
                },
            ],
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_create_check_200():
    response = client.post(
        url="/checkoutShift/createCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        json={
            "sum": 12345,
            "cashRegisterCheckNumber": "21111111",
            "fiscalDocumentNumber": "111111111",
            "typeOperation": 0,
            "taxSystem": 0,
            "typePayment": 0,
            "positions": [
                {
                    "productId": "4921975f-98bd-48f9-a700-992bee0bd738",
                    "count": 1,
                    "price": 12300,
                },
                {
                    "productId": "fa049770-62be-4036-89ce-69fdbaeb8978",
                    "count": 1,
                    "price": 45,
                },
            ],
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["sum"] == 12345
    assert len(response.json()["positions"]) == 2


@pytest.mark.worker
async def test_worker_create_check_401():
    response = client.post(
        url="/checkoutShift/createCashReceipt",
        json={
            "sum": 12345,
            "cashRegisterCheckNumber": "21111111",
            "fiscalDocumentNumber": "111111111",
            "typeOperation": 0,
            "taxSystem": 0,
            "typePayment": 0,
            "positions": [
                {
                    "productId": "4921975f-98bd-48f9-a700-992bee0bd738",
                    "count": 1,
                    "price": 12300,
                },
                {
                    "productId": "fa049770-62be-4036-89ce-69fdbaeb8978",
                    "count": 1,
                    "price": 45,
                },
            ],
        },
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_create_check_403():
    response = client.post(
        url="/checkoutShift/createCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "9a4a8e01-cdb1-4556-aa3b-215297fyq32a",
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        json={
            "sum": 12345,
            "cashRegisterCheckNumber": "21111111",
            "fiscalDocumentNumber": "111111111",
            "typeOperation": 0,
            "taxSystem": 0,
            "typePayment": 0,
            "positions": [
                {
                    "productId": "4921975f-98bd-48f9-a700-992bee0bd738",
                    "count": 1,
                    "price": 12300,
                },
                {
                    "productId": "fa049770-62be-4036-89ce-69fdbaeb8978",
                    "count": 1,
                    "price": 45,
                },
            ],
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.client
async def test_client_close_check_200():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == CheckStatuses.CLOSED.value


@pytest.mark.client
async def test_client_close_check_401():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_close_check_403():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": "914a8e01-cdb1-4556-aa3b-215297f17e2a",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.client
async def test_client_close_check_404():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "91aa8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.worker
async def test_worker_close_check_200():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == CheckStatuses.CLOSED.value


@pytest.mark.worker
async def test_worker_close_check_401():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_close_check_403():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "9a4a8e01-cdb1-4556-aa3b-215297fyq32a",
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_close_check_404():
    response = client.patch(
        url="/checkoutShift/closeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9c4a8f01-cde1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.client
async def test_client_remove_check_200():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == "9a4a8e01-cdb1-4556-aa3b-215297f17e2a"


@pytest.mark.client
async def test_client_remove_check_401():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_remove_check_403():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": "914a8e01-cdb1-4556-aa3b-215297f17e2a",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.client
async def test_client_remove_check_404():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "91aa8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.worker
async def test_worker_remove_check_200():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == "9a4a8e01-cdb1-4556-aa3b-215297f17e2a"


@pytest.mark.worker
async def test_worker_remove_check_401():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_remove_check_403():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "9a4a8e01-cdb1-4556-aa3b-215297fyq32a",
            "cashReceiptId": "9a4a8e01-cdb1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_remove_check_404():
    response = client.delete(
        url="/checkoutShift/removeCashReceipt",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "cashReceiptId": "9c4a8f01-cde1-4556-aa3b-215297f17e2a",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 404
