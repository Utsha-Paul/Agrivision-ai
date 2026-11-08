import os

from preprocessing import load_data, prepare_data
from model import build_model


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "module1",
    "raw",
    "farm_data.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "module1",
    "crop_yield_mlp.keras"
)


def main():

    print("Loading dataset...")

    df = load_data(DATA_PATH)

    print(f"Dataset shape: {df.shape}")

    print("Preparing data...")

    X_train, X_test, y_train, y_test = prepare_data(df)

    print("Training samples:", X_train.shape)
    print("Testing samples:", X_test.shape)

    model = build_model(X_train.shape[1])

    model.summary()

    print("\nStarting training...\n")

    model.fit(
        X_train,
        y_train,
        validation_split=0.2,
        epochs=50,
        batch_size=256,
        verbose=1
    )

    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True
    )

    model.save(MODEL_PATH)

    print("\nModel saved successfully.")
    print(MODEL_PATH)


if __name__ == "__main__":
    main()