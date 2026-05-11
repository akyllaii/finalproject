from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_products():
    res = client.get("/products")
    assert res.status_code == 200