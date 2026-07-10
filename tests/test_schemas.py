from app.schemas import CarFeatures
import pytest
from pydantic import ValidationError

def test_valid_car():
    data = {
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

    car = CarFeatures(**data)
    assert car.brand == "Toyota"


def test_make_year_too_old():
    data = {
        "make_year": 1994,
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
    with pytest.raises(ValidationError):
        CarFeatures(**data)


def test_engine_cc_upper_bound():
    data = {
        "make_year": 2015,
        "engine_cc": 5000,
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
    car = CarFeatures(**data)
    assert car.brand == "Toyota"


def test_unknown_brand():
    data = {
        "make_year": 2015,
        "engine_cc": 1500,
        "owner_count": 1,
        "accidents_reported": 0,
        "mileage_kmpl": 18.5,
        "fuel_type": "Petrol",
        "brand": "Lada",
        "transmission": "Manual",
        "color": "White",
        "service_history": "Full",
        "insurance_valid": "Yes",
    }
    with pytest.raises(ValidationError):
        CarFeatures(**data)
