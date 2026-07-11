import pandas as pd
from joblib import load

def test_predict_returns_positive_number():
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
    df = pd.DataFrame([data])
    pipe = load("models/model.joblib")
    model = pipe["full"]
    pred = model.predict(df)
    assert len(pred) == 1 and pred[0] > 0