import pytest

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
def