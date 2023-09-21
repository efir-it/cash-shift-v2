import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app

client = TestClient(app)


@pytest.mark.client
async def test_client_get_cash_shift_200():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == "4415b8d5-0231-4483-af76-62390e46de25"


@pytest.mark.client
async def test_client_get_cash_shift_404():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d1-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.client
async def test_client_get_cash_shift_401():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": "8a18ebd2-6432-41d4-9936-3249c22283e3",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_get_cash_shift_403():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": "8118ebd2-6432-41d4-9936-3249c22283e3",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_get_cash_shift_200():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == "4415b8d5-0231-4483-af76-62390e46de25"


@pytest.mark.worker
async def test_worker_get_cash_shift_401():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_get_cash_shift_403():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "fa7eb782-156d-436c-aa20-392954227029",
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_get_cash_shift_404():
    response = client.get(
        url="/checkoutShift/getCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62290e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.client
async def test_client_get_cash_shifts_200():
    response = client.get(
        url="/checkoutShift/getCheckoutShifts",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workplaceId": "ca0e427d-4df3-4805-9635-175d4a2a6a57",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 200


@pytest.mark.client
async def test_client_get_cash_shifts_401():
    response = client.get(
        url="/checkoutShift/getCheckoutShifts",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workplaceId": "ca0e427d-4df3-4805-9635-175d4a2a6a57",
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_get_cash_shifts_403():
    response = client.get(
        url="/checkoutShift/getCheckoutShifts",
        params={
            "clientId": "8a88ebd2-6432-41d4-9936-3249c22282e3",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workplaceId": "ca0e427d-4df3-4805-9635-175d4a2a6a67",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_get_cash_shifts_200():
    response = client.get(
        url="/checkoutShift/getCheckoutShifts",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workplaceId": "ca0e427d-4df3-4805-9635-175d4a2a6a57",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 200


@pytest.mark.worker
async def test_worker_get_cash_shifts_401():
    response = client.get(
        url="/checkoutShift/getCheckoutShifts",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workplaceId": "ca0e427d-4df3-4805-9635-175d4a2a6a57",
        },
        headers={"Authorization": f"Bearer "},
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_get_cash_shifts_403():
    response = client.get(
        url="/checkoutShift/getCheckoutShifts",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "fa71b782-156d-436c-aa20-392954227028",
            "workplaceId": "ca0e427d-4df3-4805-9635-176d4a2a6a57",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.client
async def test_client_open_cash_shift_200():
    response = client.post(
        url="/checkoutShift/openCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
        json={
            "storeId": "91deea3b-1e2e-4e13-ac2a-05d8596c51fa",
            "workplaceId": "7d556f33-9ad1-4597-83ab-74eadc613d18",
            "cashRegistrId": "ae29ed81-e7bd-4f43-aadd-234a9927b783",
        },
    )
    body = response.json()
    assert response.status_code == 200
    assert body["clientId"] == settings.TEST_CLIENT_ID
    assert body["closed"] == False


@pytest.mark.client
async def test_client_open_cash_shift_401():
    response = client.post(
        url="/checkoutShift/openCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
        },
        json={
            "storeId": "91deea3b-1e2e-4e13-ac2a-05d8596c51fa",
            "workplaceId": "7d556f33-9ad1-4597-83ab-74eadc613d18",
            "cashRegistrId": "ae29ed81-e7bd-4f43-aadd-234a9927b783",
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_open_cash_shift_403():
    response = client.post(
        url="/checkoutShift/openCheckoutShift",
        params={
            "clientId": "8a88ebd2-6432-41d3-9936-3249c22283e3",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
        json={
            "storeId": "91deea3b-1e2e-4e13-ac2a-05d8596c51fa",
            "workplaceId": "7d556f33-9ad1-4597-83ab-74eadc613d18",
            "cashRegistrId": "ae29ed81-e7bd-4f43-aadd-234a9927b783",
        },
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_open_cash_shift_200():
    response = client.post(
        url="/checkoutShift/openCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
        json={
            "storeId": "91deea3b-1e2e-4e13-ac2a-05d8596c51fa",
            "workplaceId": "7d556f33-9ad1-4597-83ab-74eadc613d18",
            "cashRegistrId": "ae29ed81-e7bd-4f43-aadd-234a9927b783",
        },
    )
    body = response.json()
    assert response.status_code == 200
    assert body["clientId"] == settings.TEST_CLIENT_ID
    assert body["closed"] == False
    assert body["workerId"] == settings.TEST_WORKER_ID


@pytest.mark.worker
async def test_worker_open_cash_shift_401():
    response = client.post(
        url="/checkoutShift/openCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
        },
        json={
            "storeId": "91deea3b-1e2e-4e13-ac2a-05d8596c51fa",
            "workplaceId": "7d556f33-9ad1-4597-83ab-74eadc613d18",
            "cashRegistrId": "ae29ed81-e7bd-4f43-aadd-234a9927b783",
        },
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_open_cash_shift_403():
    response = client.post(
        url="/checkoutShift/openCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "fa71b782-156d-436c-aa20-392954227028",
            "workerId": settings.TEST_WORKER_ID,
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
        json={
            "storeId": "91deea3b-1e2e-4e13-ac2a-05d8596c51fa",
            "workplaceId": "7d556f33-9ad1-4597-83ab-74eadc613d18",
            "cashRegistrId": "ae29ed81-e7bd-4f43-aadd-234a9927b783",
        },
    )
    assert response.status_code == 403


@pytest.mark.client
async def test_client_close_cash_shift_200():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["closed"] == True


@pytest.mark.client
async def test_client_close_cash_shift_401():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
    )
    assert response.status_code == 401


@pytest.mark.client
async def test_client_close_cash_shift_403():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": "8a88ebd2-6432-41d3-9936-3249c22283e3",
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.client
async def test_client_close_cash_shift_404():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0221-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_CLIENT_TOKEN}"},
    )
    assert response.status_code == 404


@pytest.mark.worker
async def test_worker_close_cash_shift_200():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json()["closed"] == True


@pytest.mark.worker
async def test_worker_close_cash_shift_401():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
    )
    assert response.status_code == 401


@pytest.mark.worker
async def test_worker_close_cash_shift_403():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": "4415b8d5-0231-4483-af76-62e90346de25",
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4415b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 403


@pytest.mark.worker
async def test_worker_close_cash_shift_404():
    response = client.patch(
        url="/checkoutShift/closeCheckoutShift",
        params={
            "clientId": settings.TEST_CLIENT_ID,
            "organizationId": settings.TEST_ORGANIZATION_ID,
            "workerId": settings.TEST_WORKER_ID,
            "checkoutShiftId": "4411b8d5-0231-4483-af76-62390e46de25",
        },
        headers={"Authorization": f"Bearer {settings.TEST_WORKER_TOKEN}"},
    )
    assert response.status_code == 404
