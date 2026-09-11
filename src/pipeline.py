from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline


def build_preprocessor(num_cols, cat_cols):
    num_pipe = Pipeline([("scale", StandardScaler())])
    cat_pipe = Pipeline(
        [
            (
                "ohe",
                OneHotEncoder(
                    drop="first", handle_unknown="ignore", sparse_output=False
                ),
            )
        ]
    )
    return ColumnTransformer(
        [("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)], remainder="drop"
    )


def build_pipeline(preprocessor, model):
    return Pipeline([("preprocess", preprocessor), ("model", model)])
