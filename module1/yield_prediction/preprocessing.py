import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


NUMERICAL_FEATURES = [
    "rainfall_mm",
    "avg_temp_c",
    "humidity_pct",
    "soil_ph",
    "nitrogen_kg_ha",
    "phosphorus_kg_ha",
    "potassium_kg_ha",
    "irrigation_mm",
    "days_from_last_harvest",
    "pest_index"
]

CATEGORICAL_FEATURES = [
    "soil_type",
    "crop_type",
    "fertilized",
    "weather_zone",
    "seed_quality",
    "irrigation_method",
    "season"
]

TARGET = "crop_yield_tons"


def load_data(path):
    return pd.read_csv(path)


def prepare_data(df):

    features = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

    df = df.dropna(subset=[TARGET]).copy()

    X = df[features]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    numerical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ])

    preprocessor = ColumnTransformer([
        (
            "numerical",
            numerical_pipeline,
            NUMERICAL_FEATURES
        ),
        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_FEATURES
        )
    ])

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    os.makedirs("models/module1", exist_ok=True)

    joblib.dump(
        preprocessor,
        "models/module1/preprocessor.pkl"
    )

    return X_train, X_test, y_train, y_test