import os

import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "forecasting",
    "indian_crop_weather.csv"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "forecasting",
    "lstm_scaler.pkl"
)


FEATURES = [
    "Yield_kg_per_ha",
    "Area_ha",
    "N_req_kg_per_ha",
    "P_req_kg_per_ha",
    "K_req_kg_per_ha",
    "Temperature_C",
    "Humidity_%",
    "pH",
    "Rainfall_mm",
    "Wind_Speed_m_s",
    "Solar_Radiation_MJ_m2_day"
]

TARGET = "Yield_kg_per_ha"

SEQUENCE_LENGTH = 5


def load_dataset():

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found:\n{DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print(
        f"Dataset loaded: {df.shape[0]} rows"
    )

    return df


def prepare_sequences(
    df,
    sequence_length=SEQUENCE_LENGTH
):

    df = df.copy()

    df = df.sort_values(
        [
            "Dist Code",
            "Crop",
            "Year"
        ]
    )

    # Keep only required columns
    required_columns = [
        "Dist Code",
        "Crop",
        "Year"
    ] + FEATURES

    df = df[
        required_columns
    ].dropna()

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        df[FEATURES]
    )

    scaled_df = pd.DataFrame(
        scaled_features,
        columns=FEATURES,
        index=df.index
    )

    X = []
    y = []

    groups = df.groupby(
        [
            "Dist Code",
            "Crop"
        ]
    )

    for _, group in groups:

        indices = group.index.tolist()

        if len(indices) <= sequence_length:
            continue

        for i in range(
            sequence_length,
            len(indices)
        ):

            sequence_indices = (
                indices[
                    i - sequence_length:i
                ]
            )

            target_index = indices[i]

            sequence = scaled_df.loc[
                sequence_indices
            ].values

            target = scaled_df.loc[
                target_index,
                TARGET
            ]

            X.append(
                sequence
            )

            y.append(
                target
            )

    X = np.asarray(
        X,
        dtype=np.float32
    )

    y = np.asarray(
        y,
        dtype=np.float32
    )

    os.makedirs(
        os.path.dirname(
            SCALER_PATH
        ),
        exist_ok=True
    )

    joblib.dump(
        scaler,
        SCALER_PATH
    )

    print(
        f"Sequences created: {len(X)}"
    )

    print(
        f"Sequence shape: {X.shape}"
    )

    return X, y, scaler