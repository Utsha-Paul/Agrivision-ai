import tensorflow as tf

from tensorflow.keras import Sequential
from tensorflow.keras.layers import (
    LSTM,
    Dense,
    Dropout
)


def build_lstm_model(
    sequence_length,
    num_features
):

    model = Sequential(
        [
            LSTM(
                128,
                return_sequences=True,
                input_shape=(
                    sequence_length,
                    num_features
                )
            ),

            Dropout(0.2),

            LSTM(
                64,
                return_sequences=False
            ),

            Dropout(0.2),

            Dense(
                32,
                activation="relu"
            ),

            Dense(
                1,
                activation="linear"
            )
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="mse",
        metrics=[
            "mae"
        ]
    )

    return model