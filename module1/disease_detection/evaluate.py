import os
import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from tensorflow.keras.models import load_model


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

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "disease",
    "disease_efficientnet.keras"
)

CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "models",
    "disease",
    "class_names.json"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "disease"
)

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
SEED = 42


def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    print("================================")
    print("AGRIVISION AI")
    print("DISEASE MODEL EVALUATION")
    print("================================")

    print("\nLoading model...")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found:\n{MODEL_PATH}"
        )

    model = load_model(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    print("\nLoading class names...")

    if not os.path.exists(CLASS_NAMES_PATH):
        raise FileNotFoundError(
            f"Class names file not found:\n{CLASS_NAMES_PATH}"
        )

    with open(
        CLASS_NAMES_PATH,
        "r"
    ) as f:
        class_names = json.load(f)

    num_classes = len(class_names)

    print(
        f"Number of classes: {num_classes}"
    )

    print("\nLoading validation dataset...")

    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(
            f"Dataset directory not found:\n{DATA_DIR}"
        )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=VALIDATION_SPLIT,
        subset="validation",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="int",
        shuffle=False
    )

    dataset_class_names = val_ds.class_names

    if dataset_class_names != class_names:
        print("\nWARNING:")
        print(
            "Class names in the dataset and saved class_names.json "
            "do not match."
        )

        print("\nSaved class names:")
        print(class_names)

        print("\nDataset class names:")
        print(dataset_class_names)

        raise ValueError(
            "Class-name mismatch detected."
        )

    val_ds = val_ds.prefetch(
        tf.data.AUTOTUNE
    )

    print(
        f"\nValidation dataset loaded with "
        f"{num_classes} classes."
    )

    print("\nGenerating predictions...")

    predictions = model.predict(
        val_ds,
        verbose=1
    )

    predicted_classes = np.argmax(
        predictions,
        axis=1
    )

    true_classes = np.concatenate(
        [
            labels.numpy()
            for _, labels in val_ds
        ]
    )

    print("\nPrediction generation completed.")

    labels = list(
        range(num_classes)
    )

    accuracy = accuracy_score(
        true_classes,
        predicted_classes
    )

    print("\n================================")
    print("OVERALL RESULTS")
    print("================================")

    print(
        f"\nValidation Accuracy: "
        f"{accuracy * 100:.2f}%"
    )

    present_classes = sorted(
        np.unique(true_classes)
    )

    missing_classes = sorted(
        set(labels) - set(present_classes)
    )

    print(
        f"Classes present in validation: "
        f"{len(present_classes)}/{num_classes}"
    )

    if missing_classes:

        print(
            "\nWARNING: The following classes "
            "have no validation samples:"
        )

        for class_id in missing_classes:
            print(
                f"{class_id}: "
                f"{class_names[class_id]}"
            )

    else:

        print(
            "\nAll classes are present "
            "in the validation dataset."
        )

    print("\n================================")
    print("CLASSIFICATION REPORT")
    print("================================\n")

    report = classification_report(
        true_classes,
        predicted_classes,
        labels=labels,
        target_names=class_names,
        output_dict=True,
        zero_division=0
    )

    print(
        classification_report(
            true_classes,
            predicted_classes,
            labels=labels,
            target_names=class_names,
            zero_division=0
        )
    )

    report_path = os.path.join(
        OUTPUT_DIR,
        "classification_report.json"
    )

    with open(
        report_path,
        "w"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

    print(
        f"Classification report saved to:\n"
        f"{report_path}"
    )

    macro_precision = report[
        "macro avg"
    ]["precision"]

    macro_recall = report[
        "macro avg"
    ]["recall"]

    macro_f1 = report[
        "macro avg"
    ]["f1-score"]

    weighted_precision = report[
        "weighted avg"
    ]["precision"]

    weighted_recall = report[
        "weighted avg"
    ]["recall"]

    weighted_f1 = report[
        "weighted avg"
    ]["f1-score"]

    metrics = {
        "validation_accuracy": float(
            accuracy
        ),
        "validation_accuracy_percent": float(
            accuracy * 100
        ),
        "macro_precision": float(
            macro_precision
        ),
        "macro_recall": float(
            macro_recall
        ),
        "macro_f1_score": float(
            macro_f1
        ),
        "weighted_precision": float(
            weighted_precision
        ),
        "weighted_recall": float(
            weighted_recall
        ),
        "weighted_f1_score": float(
            weighted_f1
        ),
        "num_classes": num_classes,
        "validation_classes_present": len(
            present_classes
        ),
        "validation_classes_missing": len(
            missing_classes
        ),
        "classes": class_names
    }

    metrics_path = os.path.join(
        OUTPUT_DIR,
        "metrics.json"
    )

    with open(
        metrics_path,
        "w"
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4
        )

    print(
        f"\nMetrics saved to:\n"
        f"{metrics_path}"
    )

    print("\n================================")
    print("GENERATING CONFUSION MATRIX")
    print("================================")

    cm = confusion_matrix(
        true_classes,
        predicted_classes,
        labels=labels
    )

    cm_path = os.path.join(
        OUTPUT_DIR,
        "confusion_matrix.png"
    )

    plt.figure(
        figsize=(22, 20)
    )

    plt.imshow(
        cm,
        interpolation="nearest"
    )

    plt.title(
        "AgriVision AI - Disease Detection Confusion Matrix"
    )

    plt.colorbar()

    plt.xticks(
        np.arange(num_classes),
        class_names,
        rotation=90,
        fontsize=7
    )

    plt.yticks(
        np.arange(num_classes),
        class_names,
        fontsize=7
    )

    plt.xlabel(
        "Predicted Class"
    )

    plt.ylabel(
        "True Class"
    )

    plt.tight_layout()

    plt.savefig(
        cm_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Confusion matrix saved to:\n"
        f"{cm_path}"
    )

    print("\n================================")
    print("EVALUATION SUMMARY")
    print("================================")

    print(
        f"Accuracy          : "
        f"{accuracy * 100:.2f}%"
    )

    print(
        f"Macro Precision   : "
        f"{macro_precision * 100:.2f}%"
    )

    print(
        f"Macro Recall      : "
        f"{macro_recall * 100:.2f}%"
    )

    print(
        f"Macro F1 Score    : "
        f"{macro_f1 * 100:.2f}%"
    )

    print(
        f"Weighted F1 Score : "
        f"{weighted_f1 * 100:.2f}%"
    )

    print(
        f"Classes           : "
        f"{num_classes}"
    )

    print(
        f"Validation classes: "
        f"{len(present_classes)}"
    )

    print("\n================================")
    print("EVALUATION COMPLETED")
    print("================================")

    print(
        f"\nAll results saved in:\n"
        f"{OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()