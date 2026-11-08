import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input


def build_model(input_size):

    model = Sequential([
        Input(shape=(input_size,)),

        Dense(128, activation="relu"),
        Dense(64, activation="relu"),
        Dense(32, activation="relu"),

        Dense(1, activation="linear")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="mse",
        metrics=["mae"]
    )

    return model