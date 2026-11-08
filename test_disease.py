from module1.disease_detection.predict import predict_disease


IMAGE_PATH = r"C:\Users\utsha\Downloads\Agrovision\Agrovision\AgriVisionAI\data\disease\train\Tomato___Tomato_Yellow_Leaf_Curl_Virus\c8ae615f-6d9d-4d4b-b459-983224902369___UF.GRC_YLCV_Lab 02632.JPG"


result = predict_disease(
    IMAGE_PATH
)


print("\n========================================")
print("          AGRIVISION AI")
print("       DISEASE DETECTION")
print("========================================")

print(
    f"\nCrop: {result['crop']}"
)

print(
    f"Disease: {result['disease']}"
)

print(
    f"Confidence: {result['confidence']:.2f}%"
)

print(
    f"Status: {result['status']}"
)

print("\nTop 3 Predictions:")

for index, prediction in enumerate(
    result["top_predictions"],
    start=1
):

    print(
        f"{index}. "
        f"{prediction['class']} - "
        f"{prediction['confidence']:.2f}%"
    )

print("\n========================================")