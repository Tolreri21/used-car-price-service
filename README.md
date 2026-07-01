# Car Price Predictor

A web service that predicts a car's price from its characteristics.
A machine learning model (RandomForest) is trained on a used-car dataset,
and the result is served through a REST API and a simple web UI.

## Stack

- **Python 3.10+**
- **FastAPI** + **Uvicorn** — API and static file serving
- **scikit-learn** — model training (RandomForestRegressor)
- **pandas / numpy** — data processing
- **joblib** — saving and loading model artifacts
- **PostgreSQL** + **SQLModel** — prediction history storage *(work in progress)*
- **Docker / docker-compose** — containerization

## Project structure

```
app/
  main.py          # FastAPI app: /predict, /, /app endpoints
  schemas.py       # Pydantic schema of input features (CarFeatures)
  static/          # Frontend: landing page and prediction page
ml/
  train.py         # Model training script
notebooks/
  eda.ipynb        # Exploratory data analysis
data/              # Dataset (cars.csv, gitignored)
models/            # Model artifact (model.joblib, gitignored)
docker/
  Dockerfile
  docker-compose.yml   # PostgreSQL for prediction history
pyproject.toml
requirements.txt
```

## Quick start

The project uses [uv](https://github.com/astral-sh/uv) (there's a `uv.lock`).

```bash
# install dependencies
uv sync

# train the model (creates models/model.joblib)
cd ml
uv run python train.py
cd ..

# run the service
uv run uvicorn app.main:app --reload
```

The service starts at `http://127.0.0.1:8000`:

- `/` — landing page
- `/app` — prediction form page
- `/predict` — POST API endpoint

> Running the project requires `data/cars.csv` (for training) and
> `models/model.joblib` (for the service). Both are gitignored, so the
> model must be trained locally before starting the service.

## API

### `POST /predict`

Takes a car's characteristics and returns the predicted price in USD.

**Request body:**

```json
{
  "make_year": 2015,
  "engine_cc": 1600,
  "owner_count": 2,
  "accidents_reported": 0,
  "mileage_kmpl": 18.5,
  "fuel_type": "Petrol",
  "brand": "Toyota",
  "transmission": "Manual",
  "color": "White",
  "service_history": "Full",
  "insurance_valid": "Yes"
}
```

**Response:**

```json
{ "predicted_price": 12450.37 }
```

Example request via curl:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"make_year":2015,"engine_cc":1600,"owner_count":2,"accidents_reported":0,"mileage_kmpl":18.5,"fuel_type":"Petrol","brand":"Toyota","transmission":"Manual","color":"White","service_history":"Full","insurance_valid":"Yes"}'
```

Interactive documentation is available at `/docs` (Swagger UI).

## Docker

Build and run the service:

```bash
docker build -f docker/Dockerfile -t car-price .
docker run -p 8000:8000 car-price
```

Start the database for prediction history:

```bash
docker compose -f docker/docker-compose.yml up -d
```

PostgreSQL will be available on port `5432` (database `prediction_history`).

## How the model works

1. `ml/train.py` reads `data/cars.csv` and drops missing values.
2. Numeric features are scaled with `StandardScaler`, categorical ones are
   encoded with `OneHotEncoder`.
3. A `RandomForestRegressor` is trained; quality is measured with RMSE and MAE.
4. The model, encoder, scaler, and column lists are saved to
   `models/model.joblib`.
5. On app startup (`lifespan`) the artifacts are loaded into memory and
   reused on every `/predict` request.

## Status

- [x] Model training
- [x] Prediction API
- [x] Static frontend (landing + form)
- [x] Dockerfile
- [ ] Saving prediction history to PostgreSQL *(current branch `feat/prediction-history`)*
- [ ] Authentication
- [ ] Deployment
