from fastapi.testclient import TestClient
from app.main import app


def test_predict():
    payload = {
        "make_year": 2015,
        "engine_cc": 1500,
        "owner_count": 1,
        "accidents_reported": 0,
        "mileage_kmpl": 18.5,
        "fuel_type": "Petrol",
        "brand": "Toyota",
        "transmission": "Manual",
        "color": "White",
        "service_history": "Full",
        "insurance_valid": "Yes",
    }
    with TestClient(app) as client:
        response = client.post("/predict" , json= payload)
    assert response.status_code == 200

