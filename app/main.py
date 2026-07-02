from contextlib import asynccontextmanager

import numpy as np
import pandas as pd
from joblib import load
from fastapi import FastAPI , Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import CarFeatures
from app.db import create_db_and_tables , get_session
from sqlmodel import Session
from app.models import PredictionHistory

ml = {}

@asynccontextmanager
async def lifespan(app : FastAPI):
    artifacts = load("models/model.joblib")
    ml["model"]   = artifacts["model"]
    ml["encoder"] = artifacts["encoder"]
    ml["scaler"]  = artifacts["scaler"]
    ml["cat"] = artifacts["cat_cols"]
    ml["num"] = artifacts["num_cols"]
    create_db_and_tables()
    yield
    ml.clear()

app = FastAPI(lifespan=lifespan)

app.mount("/static" , StaticFiles(directory="app/static"),name = "static")

@app.post("/predict")
def predict(car : CarFeatures,session : Session = Depends(get_session)):
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

    row = PredictionHistory(**car.model_dump() , predicted_price = float(pred[0]))

    session.add(row)
    session.commit()
    return {"predicted_price" : float(pred[0])}

@app.get("/")
def index():
    return FileResponse("app/static/index.html")

@app.get("/app")
def app_page():
    return FileResponse("app/static/app.html")