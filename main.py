import tkinter as tk
from tkinter import filedialog, messagebox

from module1.yield_prediction.predict import predict_crop_yield
from module1.disease_detection.predict import predict_disease


def select_leaf_image():

    return filedialog.askopenfilename(
        title="Select Leaf Image",
        filetypes=[
            (
                "Image Files",
                "*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG"
            ),
            (
                "All Files",
                "*.*"
            )
        ]
    )


def create_entry(parent, label, row, default=""):

    tk.Label(
        parent,
        text=label,
        anchor="w"
    ).grid(
        row=row,
        column=0,
        padx=10,
        pady=6,
        sticky="w"
    )

    entry = tk.Entry(
        parent,
        width=30
    )

    entry.grid(
        row=row,
        column=1,
        padx=10,
        pady=6
    )

    if default != "":
        entry.insert(
            0,
            default
        )

    return entry


def create_dropdown(
    parent,
    label,
    row,
    values
):

    tk.Label(
        parent,
        text=label,
        anchor="w"
    ).grid(
        row=row,
        column=0,
        padx=10,
        pady=6,
        sticky="w"
    )

    variable = tk.StringVar(
        value=values[0]
    )

    dropdown = tk.OptionMenu(
        parent,
        variable,
        *values
    )

    dropdown.config(
        width=27
    )

    dropdown.grid(
        row=row,
        column=1,
        padx=10,
        pady=6
    )

    return variable


def analyze():

    try:

        rainfall = float(
            rainfall_entry.get()
        )

        temperature = float(
            temperature_entry.get()
        )

        humidity = float(
            humidity_entry.get()
        )

        soil_ph = float(
            soil_ph_entry.get()
        )

        nitrogen = float(
            nitrogen_entry.get()
        )

        phosphorus = float(
            phosphorus_entry.get()
        )

        potassium = float(
            potassium_entry.get()
        )

        irrigation = float(
            irrigation_entry.get()
        )

        harvest_days = float(
            harvest_days_entry.get()
        )

        pest_index = float(
            pest_index_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numeric values."
        )

        return


    if not leaf_image_path.get():

        messagebox.showerror(
            "Missing Image",
            "Please upload a leaf image."
        )

        return


    try:

        yield_result = predict_crop_yield(

            rainfall_mm=rainfall,

            avg_temp_c=temperature,

            humidity_pct=humidity,

            soil_ph=soil_ph,

            nitrogen_kg_ha=nitrogen,

            phosphorus_kg_ha=phosphorus,

            potassium_kg_ha=potassium,

            irrigation_mm=irrigation,

            days_from_last_harvest=harvest_days,

            pest_index=pest_index,

            soil_type=soil_type.get(),

            crop_type=crop_type.get(),

            fertilized=fertilized.get(),

            weather_zone=weather_zone.get(),

            seed_quality=seed_quality.get(),

            irrigation_method=irrigation_method.get(),

            season=season.get()
        )


        disease_result = predict_disease(
            leaf_image_path.get()
        )


        if isinstance(
            yield_result,
            dict
        ):

            yield_value = yield_result[
                "predicted_yield_tons_per_hectare"
            ]

            yield_crop = yield_result[
                "crop"
            ]

            yield_category = yield_result[
                "yield_category"
            ]

        else:

            yield_value = float(
                yield_result
            )

            yield_crop = crop_type.get()

            if yield_value < 2:

                yield_category = "Low"

            elif yield_value < 4:

                yield_category = "Moderate"

            elif yield_value < 6:

                yield_category = "Good"

            else:

                yield_category = "High"


        detected_crop = disease_result[
            "crop"
        ]


        crop_match = (

            yield_crop.lower().strip()

            ==

            detected_crop.lower().strip()

        )


        result_text.delete(
            "1.0",
            tk.END
        )


        result_text.insert(
            tk.END,
            "========================================\n"
        )

        result_text.insert(
            tk.END,
            "          AGRIVISION AI\n"
        )

        result_text.insert(
            tk.END,
            "           MODULE 1\n"
        )

        result_text.insert(
            tk.END,
            "========================================\n\n"
        )


        result_text.insert(
            tk.END,
            "--------------- YIELD ------------------\n\n"
        )

        result_text.insert(
            tk.END,
            f"Crop: {yield_crop}\n"
        )

        result_text.insert(
            tk.END,
            f"Predicted Yield: "
            f"{yield_value:.3f} tons/hectare\n"
        )

        result_text.insert(
            tk.END,
            f"Yield Category: "
            f"{yield_category}\n\n"
        )


        result_text.insert(
            tk.END,
            "-------------- DISEASE -----------------\n\n"
        )

        result_text.insert(
            tk.END,
            f"Detected Crop: "
            f"{detected_crop}\n"
        )

        result_text.insert(
            tk.END,
            f"Disease: "
            f"{disease_result['disease']}\n"
        )

        result_text.insert(
            tk.END,
            f"Confidence: "
            f"{disease_result['confidence']:.2f}%\n"
        )

        result_text.insert(
            tk.END,
            f"Status: "
            f"{disease_result['status']}\n\n"
        )


        result_text.insert(
            tk.END,
            "---------- CROP VALIDATION -------------\n\n"
        )


        if crop_match:

            result_text.insert(
                tk.END,
                "Crop Consistency: VERIFIED\n"
            )

            result_text.insert(
                tk.END,
                f"Farm Crop: {yield_crop}\n"
            )

            result_text.insert(
                tk.END,
                f"Detected Crop: {detected_crop}\n\n"
            )

        else:

            result_text.insert(
                tk.END,
                "Crop Consistency: WARNING\n"
            )

            result_text.insert(
                tk.END,
                f"Farm Crop: {yield_crop}\n"
            )

            result_text.insert(
                tk.END,
                f"Detected Crop: {detected_crop}\n\n"
            )

            result_text.insert(
                tk.END,
                "WARNING:\n"
            )

            result_text.insert(
                tk.END,
                "The uploaded leaf image appears "
                "to belong to a different crop.\n\n"
            )


        result_text.insert(
            tk.END,
            "---------- TOP 3 PREDICTIONS ------------\n\n"
        )


        for index, prediction in enumerate(
            disease_result["top_predictions"],
            start=1
        ):

            result_text.insert(
                tk.END,
                f"{index}. "
                f"{prediction['class']} - "
                f"{prediction['confidence']:.2f}%\n"
            )


        result_text.insert(
            tk.END,
            "\n========================================\n"
        )

        result_text.insert(
            tk.END,
            "        MODULE 1 COMPLETED\n"
        )

        result_text.insert(
            tk.END,
            "========================================\n"
        )

    except Exception as error:

        messagebox.showerror(
            "Prediction Error",
            str(error)
        )


def upload_image():

    path = select_leaf_image()

    if path:

        leaf_image_path.set(
            path
        )

        image_label.config(
            text="Leaf image selected"
        )


root = tk.Tk()

root.title(
    "AgriVision AI - Module 1"
)

root.geometry(
    "1000x900"
)

root.resizable(
    False,
    False
)


title = tk.Label(
    root,
    text="AGRIVISION AI",
    font=("Arial", 24, "bold")
)

title.pack(
    pady=(15, 0)
)


subtitle = tk.Label(
    root,
    text="Intelligent Crop & Disease Analysis",
    font=("Arial", 12)
)

subtitle.pack(
    pady=(0, 15)
)


main_frame = tk.Frame(
    root
)

main_frame.pack(
    fill="both",
    expand=True
)


input_frame = tk.LabelFrame(
    main_frame,
    text="Farm Information",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)

input_frame.pack(
    side="left",
    fill="y",
    padx=15,
    pady=10
)


result_frame = tk.LabelFrame(
    main_frame,
    text="Analysis Result",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=10
)

result_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


crop_type = create_dropdown(
    input_frame,
    "Crop",
    0,
    [
        "Rice",
        "Wheat",
        "Maize",
        "Tomato",
        "Potato",
        "Apple",
        "Grape",
        "Pepper",
        "Peach",
        "Cherry"
    ]
)


season = create_dropdown(
    input_frame,
    "Season",
    1,
    [
        "Kharif",
        "Rabi",
        "Zaid"
    ]
)


soil_type = create_dropdown(
    input_frame,
    "Soil Type",
    2,
    [
        "Loamy",
        "Clay",
        "Sandy",
        "Silty",
        "Black",
        "Red"
    ]
)


fertilized = create_dropdown(
    input_frame,
    "Fertilized",
    3,
    [
        "Yes",
        "No"
    ]
)


weather_zone = create_dropdown(
    input_frame,
    "Weather Zone",
    4,
    [
        "Tropical",
        "Temperate",
        "Arid",
        "Semi-Arid",
        "Humid"
    ]
)


seed_quality = create_dropdown(
    input_frame,
    "Seed Quality",
    5,
    [
        "High",
        "Medium",
        "Low"
    ]
)


irrigation_method = create_dropdown(
    input_frame,
    "Irrigation Method",
    6,
    [
        "Drip",
        "Sprinkler",
        "Flood",
        "Rainfed"
    ]
)


rainfall_entry = create_entry(
    input_frame,
    "Rainfall (mm)",
    7,
    "120"
)


temperature_entry = create_entry(
    input_frame,
    "Temperature (°C)",
    8,
    "27"
)


humidity_entry = create_entry(
    input_frame,
    "Humidity (%)",
    9,
    "71"
)


soil_ph_entry = create_entry(
    input_frame,
    "Soil pH",
    10,
    "6.5"
)


nitrogen_entry = create_entry(
    input_frame,
    "Nitrogen (kg/ha)",
    11,
    "72"
)


phosphorus_entry = create_entry(
    input_frame,
    "Phosphorus (kg/ha)",
    12,
    "45"
)


potassium_entry = create_entry(
    input_frame,
    "Potassium (kg/ha)",
    13,
    "60"
)


irrigation_entry = create_entry(
    input_frame,
    "Irrigation (mm)",
    14,
    "80"
)


harvest_days_entry = create_entry(
    input_frame,
    "Days Since Harvest",
    15,
    "30"
)


pest_index_entry = create_entry(
    input_frame,
    "Pest Index",
    16,
    "10"
)


leaf_image_path = tk.StringVar()


upload_button = tk.Button(
    input_frame,
    text="Upload Leaf Image",
    command=upload_image,
    width=30,
    height=2
)

upload_button.grid(
    row=17,
    column=0,
    columnspan=2,
    pady=(15, 5)
)


image_label = tk.Label(
    input_frame,
    text="No image selected",
    wraplength=250
)

image_label.grid(
    row=18,
    column=0,
    columnspan=2,
    pady=5
)


result_text = tk.Text(
    result_frame,
    width=55,
    height=42,
    font=("Consolas", 10),
    wrap="word"
)

result_text.pack(
    fill="both",
    expand=True
)


control_frame = tk.Frame(
    root
)

control_frame.pack(
    fill="x",
    padx=15,
    pady=(0, 15)
)


analyze_button = tk.Button(
    control_frame,
    text="ANALYZE CROP",
    command=analyze,
    width=35,
    height=2,
    font=("Arial", 12, "bold")
)

analyze_button.pack(
    pady=5
)


root.mainloop()