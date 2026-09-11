from sklearn.linear_model import Ridge

from src.data import load_raw, get_columns, split_data
from src.pipeline import build_preprocessor, build_pipeline


def test_load_raw_splits_target():
    X, y = load_raw("data/cars.csv")
    assert "price_usd" not in X.columns
    assert len(X) == len(y)
    assert X["service_history"].isna().sum() == 0


def test_split_data_keeps_all_rows():
    X, y = load_raw("data/cars.csv")
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)
    assert len(X_train) + len(X_val) + len(X_test) == len(X)
    assert len(y_train) + len(y_val) + len(y_test) == len(y)


def test_pipeline_predicts_positive_number():
    X, y = load_raw("data/cars.csv")
    num_cols, cat_cols = get_columns(X)
    pipe = build_pipeline(build_preprocessor(num_cols, cat_cols), Ridge(random_state=42))
    pipe.fit(X, y)
    pred = pipe.predict(X.head(1))
    assert len(pred) == 1 and pred[0] > 0
