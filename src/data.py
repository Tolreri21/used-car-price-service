import pandas as pd
from sklearn.model_selection import train_test_split


def load_raw(path, sep=","):
    df = pd.read_csv(path, sep=sep)
    df["service_history"] = df["service_history"].fillna("Unknown")
    X = df.drop("price_usd", axis=1)
    y = df["price_usd"]
    return X, y


def get_columns(X):
    num_cols = X.select_dtypes(include="number").columns.to_list()
    cat_cols = X.select_dtypes(include="object").columns.to_list()
    return num_cols, cat_cols


def split_data(X, y, test_size=0.2, val_size=0.1765, random_state=42):
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size, random_state=random_state
    )
    return X_train, X_val, X_test, y_train, y_val, y_test
