from contextlib import asynccontextmanager

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
    pipe = load("models/model.joblib")
    ml["pipe"] = pipe
    create_db_and_tables()
    yield
    ml.clear()

app = FastAPI(lifespan=lifespan)

app.mount("/static" , StaticFiles(directory="app/static"),name = "static")

@app.post("/predict")
def predict(car : CarFeatures,session : Session = Depends(get_session)):
    car_df = pd.DataFrame([car.model_dump()])

    model = ml["pipe"]["full"]

    pred = model.predict(car_df)

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