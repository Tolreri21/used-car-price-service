from pydantic import BaseModel

class CarFeatures(BaseModel):
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

