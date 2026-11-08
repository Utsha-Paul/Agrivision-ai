import os
import json
import tensorflow as tf
import matplotlib.pyplot as plt

from model import build_model


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "disease",
    "train"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "disease"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "disease"
)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():

    print("Loading dataset...")
    print("Dataset path:")
    print(DATA_DIR)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="training",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=42,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int"
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)

    print("\n================================")
    print("DISEASE DATASET")
    print("================================")

    print("Number of classes:", num_classes)

    for i, name in enumerate(class_names):
        print(i, "->", name)

    with open(
        os.path.join(
            MODEL_DIR,
            "class_names.json"
        ),
        "w"
    ) as f:
        json.dump(class_names, f, indent=4)

    autotune = tf.data.AUTOTUNE

    train_ds = train_ds.prefetch(
        buffer_size=autotune
    )

    val_ds = val_ds.prefetch(
        buffer_size=autotune
    )

    model, base_model = build_model(
        num_classes
    )

    model.summary()

    callbacks = [

        tf.keras.callbacks.ModelCheckpoint(
            os.path.join(
                MODEL_DIR,
                "best_disease_model.keras"
            ),
            monitor="val_accuracy",
            save_best_only=True,
            mode="max"
        ),

        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=5,
            restore_best_weights=True
        ),

        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.3,
            patience=2,
            min_lr=1e-7
        )
    ]

    print("\n================================")
    print("PHASE 1: TRANSFER LEARNING")
    print("================================")

    history1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=10,
        callbacks=callbacks
    )

    print("\n================================")
    print("PHASE 2: FINE TUNING")
    print("================================")

    base_model.trainable = True

    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=1e-5
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    history2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=10,
        callbacks=callbacks
    )

    model.save(
        os.path.join(
            MODEL_DIR,
            "disease_efficientnet.keras"
        )
    )

    print("\nModel saved successfully.")

    accuracy = (
        history1.history["accuracy"]
        + history2.history["accuracy"]
    )

    val_accuracy = (
        history1.history["val_accuracy"]
        + history2.history["val_accuracy"]
    )

    loss = (
        history1.history["loss"]
        + history2.history["loss"]
    )

    val_loss = (
        history1.history["val_loss"]
        + history2.history["val_loss"]
    )

    epochs = range(
        1,
        len(accuracy) + 1
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        epochs,
        accuracy,
        label="Training Accuracy"
    )

    plt.plot(
        epochs,
        val_accuracy,
        label="Validation Accuracy"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Disease Detection Accuracy")
    plt.legend()
    plt.grid()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "accuracy.png"
        )
    )

    plt.close()

    plt.figure(figsize=(10, 6))

    plt.plot(
        epochs,
        loss,
        label="Training Loss"
    )

    plt.plot(
        epochs,
        val_loss,
        label="Validation Loss"
    )

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Disease Detection Loss")
    plt.legend()
    plt.grid()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "loss.png"
        )
    )

    plt.close()

    print("Training graphs saved.")


if __name__ == "__main__":
    main()