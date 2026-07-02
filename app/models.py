from sqlmodel import SQLModel , Field
from datetime import datetime


class PredictionHistory(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key=True)
    created_at : datetime = Field(default_factory=datetime.utcnow)
    make_year : int
    engine_cc : int
    owner_count : int
    accidents_reported : int
    mileage_kmpl : float

    fuel_type : str
    brand : str
    transmission : str
    color : str
    service_history : str
    insurance_valid : str

    predicted_price : float