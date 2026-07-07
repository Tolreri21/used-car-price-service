import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
from joblib import load, dump
from sklearn.model_selection import RandomizedSearchCV


X_train = pd.read_csv("../data/train_features.csv")
y_train = pd.read_csv("../data/train_labels.csv").squeeze("columns")

X_test = pd.read_csv("../data/test_features.csv")
y_test = pd.read_csv("../data/test_labels.csv").squeeze("columns")

X_val = pd.read_csv("../data/val_features.csv")
y_val = pd.read_csv("../data/val_labels.csv").squeeze("columns")

preprocessor = load("../models/preprocessor.joblib")

models = {
    "forest": RandomForestRegressor(random_state=42),
    "ridge": Ridge(random_state=42),
    "linear": LinearRegression(),
}

for name, model in models.items():
    print(name)
    model.fit(X_train, y_train)
    pred = model.predict(X_val)
    rmse = root_mean_squared_error(y_val, pred)
    mae = mean_absolute_error(y_val, pred)
    print(rmse)
    print(mae)


forest_params = {
    "n_estimators": [100, 300, 500],
    "max_depth": [5, 8, 12],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 5],
}

ridge_params = {
    "alpha": [0.01, 0.1, 1.0, 10.0, 100.0],
}

forest_search = RandomizedSearchCV(
    param_distributions=forest_params,
    estimator=RandomForestRegressor(random_state=42),
    n_iter=15,
    scoring="neg_root_mean_squared_error",
    cv=4,
    random_state=42,
    n_jobs=-1,
)

ridge_search = RandomizedSearchCV(
    param_distributions=ridge_params,
    estimator=Ridge(random_state=42),
    n_iter=5,
    scoring="neg_root_mean_squared_error",
    cv=4,
    random_state=42,
    n_jobs=-1,
)

full_x = pd.concat([X_train, X_val])
full_y = pd.concat([y_train, y_val])

searches = {"forest": forest_search, "ridge": ridge_search}
for name, search in searches.items():
    search.fit(full_x, full_y)
    print(name)
    print(search.best_params_)
    print(search.best_score_)

best_name = max(searches, key=lambda n: searches[n].best_score_)
best_model = searches[best_name].best_estimator_
print("Best model:")
print(best_name)

print("Best model results")
pred = best_model.predict(X_test)
rmse = root_mean_squared_error(y_test, pred)
mae = mean_absolute_error(y_test, pred)
print(f"RMSE {rmse}")
print(f"MAE {mae}")


full_pipe = Pipeline(
    [("preprocess", preprocessor["preprocessor"]), ("model", best_model)]
)

dump({"full": full_pipe}, "../models/model.joblib")
