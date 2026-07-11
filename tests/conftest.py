import pytest
from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
from joblib import load
from fastapi.testclient import TestClient
from app.main import app, ml
from app.db import get_session, create_db_and_tables


@pytest.fixture
def sample_df():
    return {
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


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    create_db_and_tables(test_engine)

    def override_get_session():
        with Session(test_engine) as session:
            yield session


    app.dependency_overrides[get_session] = override_get_session
    ml["pipe"] = load("models/model.joblib")

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
