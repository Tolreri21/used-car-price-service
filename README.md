# Carpy — Car Price Predictor

A web service that predicts a used car's price from its characteristics.
A machine learning model is trained on a used-car dataset and served through a
REST API and a small web UI. Predictions are stored in PostgreSQL.

🔗 **Live:** http://52.202.119.93 — deployed on AWS EC2 (Docker Compose).

![Carpy demo](docs/demo.gif)

## Stack

- **Python 3.10**
- **FastAPI** + **Uvicorn** — API and static file serving
- **scikit-learn** — preprocessing + model training (`ColumnTransformer`,
  `RandomForestRegressor` vs `Ridge`, `RandomizedSearchCV`)
- **pandas** — data processing
- **joblib** — saving and loading the model pipeline
- **PostgreSQL** + **SQLModel** — prediction history storage
- **Vanilla HTML/CSS/JS** — frontend, no frameworks (self-hosted IBM Plex fonts)
- **pytest** — tests (schemas, API, ML pipeline)
- **ruff** — linting
- **Docker / docker-compose** — containerization
- **GitHub Actions** — CI/CD: lint → tests → build & push → deploy

## Project structure

```
app/
  main.py          # FastAPI app: /predict, /, /app endpoints
  schemas.py       # Pydantic schema of input features (CarFeatures)
  models.py        # SQLModel table: PredictionHistory
  db.py            # DB engine + session
  static/          # Frontend: landing (/), prediction form (/app), fonts
ml/
  train.py         # Loads prepared features, tunes models, saves model.joblib
  notebooks/
    eda.ipynb            # Exploratory data analysis
    preprocessing.ipynb  # Split + fit ColumnTransformer, write features + preprocessor
tests/
  conftest.py      # Fixtures: TestClient with in-memory SQLite override
  test_schemas.py  # Input validation rules
  test_api.py      # /predict endpoint behaviour
  test_pipeline.py # Loaded model pipeline sanity checks
data/              # Dataset cars.csv + generated feature/label CSVs (gitignored)
models/            # model.joblib (committed — the service runs out of the box)
.github/workflows/
  CI-CD.yml        # ruff → pytest → docker build+push → deploy to EC2
Dockerfile
docker-compose.yml # app + db (PostgreSQL) services
pyproject.toml
requirements.txt   # pinned via `uv export`
```

## Quick start

The project uses [uv](https://github.com/astral-sh/uv) (there's a `uv.lock`).
The trained model is committed, so the service runs without any ML steps:

```bash
uv sync
cp .env.example .env               # fill in DATABASE_URL / POSTGRES_*
uv run uvicorn app.main:app --reload
```

The service starts at `http://127.0.0.1:8000`:

- `/` — landing page
- `/app` — prediction form page
- `/predict` — POST API endpoint
- `/docs` — interactive Swagger UI

### Retraining the model (optional)

Training needs `data/cars.csv`, which is gitignored:

```bash
# 1. Preprocessing: run ml/notebooks/preprocessing.ipynb
#    reads data/cars.csv, splits train/val/test, fits the ColumnTransformer,
#    writes data/*_features.csv + *_labels.csv and models/preprocessor.joblib

# 2. Train + select the model
cd ml
uv run python train.py     # tunes RandomForest & Ridge, saves models/model.joblib
```

## API

### `POST /predict`

Takes a car's characteristics and returns the predicted price in USD, and
records the request in the database.

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

## Tests

```bash
uv run pytest
```

The API tests replace the real database with an in-memory SQLite through
FastAPI dependency overrides, so no PostgreSQL is needed to run them.
Covered: schema validation rules, `/predict` happy path and error responses,
and the serialized pipeline's predictions.

## Docker

The whole stack — API (`app`) + PostgreSQL (`db`) — comes up with one command,
configured through `.env`:

```bash
docker compose up -d --build     # API on http://localhost:8000
```

The prebuilt API image (built for `linux/amd64`) is published to Docker Hub:

```bash
docker pull tolreri21/carpy:latest
```

## CI/CD

Every push to `main` runs `.github/workflows/CI-CD.yml`:

1. **Lint** — `ruff check .`
2. **Tests** — `pytest` via uv
3. **Build & push** — Docker image → Docker Hub (`tolreri21/carpy:latest`)
4. **Deploy** — SSH to the EC2 instance, `docker compose pull && up -d`

## How it works

**Preprocessing — `ml/notebooks/preprocessing.ipynb`:**

1. Reads `data/cars.csv`, fills missing `service_history` with `"Unknown"`.
2. Splits into train / validation / test.
3. Builds a `ColumnTransformer` — `StandardScaler` for numeric columns,
   `OneHotEncoder` for categorical — fits it **on the training set only**.
4. Writes the transformed feature CSVs and label CSVs to `data/`, and saves the
   fitted transformer to `models/preprocessor.joblib`.

**Training — `ml/train.py`:**

5. Loads the prepared feature/label CSVs.
6. Tunes both a `RandomForestRegressor` and a `Ridge` with `RandomizedSearchCV`
   (4-fold CV, negative RMSE).
7. Picks the champion by best CV score and evaluates it once on the held-out
   test set (RMSE / MAE).
8. Wraps the fitted preprocessor + champion model into a single sklearn
   `Pipeline` and saves it to `models/model.joblib`.

**Serving — `app/main.py`:**

9. On startup (`lifespan`) the pipeline is loaded into memory.
10. `/predict` feeds the raw request straight into the pipeline — preprocessing
    happens inside — and stores the input and prediction in PostgreSQL.

## Status

- [x] Preprocessing + model training (RandomForest vs Ridge, champion selection)
- [x] Prediction API
- [x] Prediction history in PostgreSQL (SQLModel)
- [x] Frontend: landing + prediction form (vanilla HTML/CSS/JS)
- [x] Tests: schemas, API, ML pipeline (pytest)
- [x] Dockerfile + full docker-compose stack (`app` + `db` in one command)
- [x] CI/CD: GitHub Actions → Docker Hub → AWS EC2
