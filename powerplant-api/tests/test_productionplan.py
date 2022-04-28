from fastapi.testclient import TestClient

from powerplant_api.app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Thank you for using powerplant-api!"}
