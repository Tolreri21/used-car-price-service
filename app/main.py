from contextlib import asynccontextmanager

import numpy as np
import pandas as pd
from joblib import load
from fastapi import FastAPI

from app.schemas import CarFeatures

ml = {}

@asynccontextmanager
async def lifespan(app : FastAPI):
    artifacts = load("models/model.joblib")
    ml["model"]   = artifacts["model"]
    ml["encoder"] = artifacts["encoder"]
    ml["scaler"]  = artifacts["scaler"]
    ml["cat"] = artifacts["cat_cols"]
    ml["num"] = artifacts["num_cols"]
    yield
    ml.clear()

app = FastAPI(lifespan=lifespan)

@app.post("/predict")
def predict(car : CarFeatures):
    car_df = pd.DataFrame([car.model_dump()])

    model = ml["model"]
    enc = ml["encoder"]
    scaler = ml["scaler"]
    cat_cols = ml["cat"]
    num_cols = ml["num"]



    car_n = scaler.transform(car_df[num_cols])
    car_c = enc.transform(car_df[cat_cols])

    car_predict = np.hstack([car_n , car_c])

    pred = model.predict(car_predict)
    return {"predicted_price" : float(pred[0])}
