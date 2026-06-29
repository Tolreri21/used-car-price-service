import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
import joblib

# load data inside pandas dataframe
df = pd.read_csv("../data/cars.csv")
print(df.head(5))

# preprocessing
df = df.dropna()
df.info()
scaler = StandardScaler()
enc = OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False)

# ML
x_cols = df.columns.drop("price_usd")
y = "price_usd"
print(x_cols , y)

X_train, X_test, y_train , y_test = train_test_split(df[x_cols],df[y],test_size= 0.2, random_state=42 )
model = RandomForestRegressor(random_state=42)

num_cols = X_train.select_dtypes(include="number").columns
cat_cols = X_train.select_dtypes(include="object").columns

x_t_scaled = scaler.fit_transform(X_train[num_cols])
x_t_enc    = enc.fit_transform(X_train[cat_cols])

x_test_scaled = scaler.transform(X_test[num_cols])
x_test_enc    = enc.transform(X_test[cat_cols])

X_train_prep = np.hstack([x_t_scaled, x_t_enc])
X_test_prep  = np.hstack([x_test_scaled, x_test_enc])

model.fit(X_train_prep, y_train)

prediction = model.predict(X_test_prep)
rmse = root_mean_squared_error(y_test , prediction)
mae = mean_absolute_error(y_test , prediction)
print(rmse)
print(mae)

joblib.dump({"model": model, "encoder": enc, "scaler": scaler}, "../models/model.joblib")