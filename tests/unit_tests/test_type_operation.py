from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


async def test_get_types_operation():
    response = client.get("/types_operation")
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_get_type_operation():
    response = client.get("/types_operation/1")
    assert response.status_code == 200
    assert response.json()["name"] == "type_operation_1"


async def test_post_type_operation():
    response = client.post("/types_operation", json={"name": "type_operation_4"})
    response_get = client.get("types_operation/4")
    assert response.status_code == 200
    assert response_get.status_code == 200
    assert response_get.json()["name"] == "type_operation_4"


async def test_put_type_operation():
    response = client.put("/types_operation/1", json={"name": "type_operation_1_new"})
    response_get = client.get("types_operation/1")
    assert response.status_code == 200
    assert response_get.status_code == 200
    assert response_get.json()["name"] == "type_operation_1_new"


async def test_delete_type_operation():
    response = client.delete("/types_operation/4")
    assert response.status_code == 200
