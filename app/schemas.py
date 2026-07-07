from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Literal


class CarFeaturesBase(SQLModel):
    make_year: int = Field(ge=1995, le=datetime.now().year)
    engine_cc: int = Field(ge=800, le=5000)
    owner_count: int = Field(ge=1, le=5)
    accidents_reported: int = Field(ge=0, le=5)
    mileage_kmpl: float = Field(ge=5, le=35)

    fuel_type: str
    brand: str
    transmission: str
    color: str
    service_history: str
    insurance_valid: str


class CarFeatures(CarFeaturesBase):
    fuel_type: Literal["Diesel", "Electric", "Petrol"]
    brand: Literal[
        "BMW",
        "Chevrolet",
        "Ford",
        "Honda",
        "Hyundai",
        "Kia",
        "Nissan",
        "Tesla",
        "Toyota",
        "Volkswagen",
    ]
    transmission: Literal["Automatic", "Manual"]
    color: Literal["Black", "Blue", "Gray", "Red", "Silver", "White"]
    service_history: Literal["Full", "Partial", "Unknown"]
    insurance_valid: Literal["Yes", "No"]
