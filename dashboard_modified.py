import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from module1.yield_prediction.predict import predict_crop_yield
from module1.disease_detection.predict import predict_disease

from intelligence.image_validation.validator import (
    validate_crop_image
)

from intelligence.health.health_score import (
    calculate_health_score
)

from intelligence.risk.risk_engine import (
    calculate_risk
)

from intelligence.forecast.forecast import (
    generate_forecast
)

from intelligence.recommendations.recommendation_engine import (
    generate_recommendations
)

from intelligence.spectral.preprocessing import (
    preprocess_leaf_image
)

from intelligence.spectral.analyzer import (
    analyze_leaf_spectrum
)

from intelligence.spectral.visualizer import (
    generate_stress_visualization
)

from intelligence.spectral.model.predict import predict_spectral


class AgriVisionDashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AgriVision AI"
        )

        self.root.geometry(
            "1450x920"
        )

        self.root.minsize(
            1200,
            800
        )

        self.root.configure(
            bg="#F3F6F4"
        )

        self.image_path = None
        self.preview_image = None
        self.visualization_image = None
        self.hyperleaf_result = None

        self.setup_ui()


    def setup_ui(self):

        self.create_header()

        main_container = tk.Frame(
            self.root,
            bg="#F3F6F4"
        )

        main_container.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=15
        )

        self.create_left_panel(
            main_container
        )

        self.create_right_panel(
            main_container
        )

        self.create_status_bar()


    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#173F2F",
            height=90
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        title = tk.Label(
            header,
            text="AGRIVISION AI",
            font=("Arial", 26, "bold"),
            fg="white",
            bg="#173F2F"
        )

        title.pack(
            pady=(12, 0)
        )

        subtitle = tk.Label(
            header,
            text="Unified Crop Intelligence Platform",
            font=("Arial", 11),
            fg="#D7EADF",
            bg="#173F2F"
        )

        subtitle.pack()


    def create_left_panel(
        self,
        parent
    ):

        self.left_panel = tk.LabelFrame(
            parent,
            text="FARM DATA",
            font=("Arial", 12, "bold"),
            bg="#FFFFFF",
            padx=14,
            pady=10
        )

        self.left_panel.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        self.create_inputs()


    def create_inputs(self):

        parent = self.left_panel

        self.crop = self.create_dropdown(
            parent,
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

        self.season = self.create_dropdown(
            parent,
            "Season",
            1,
            [
                "Kharif",
                "Rabi",
                "Zaid"
            ]
        )

        self.soil_type = self.create_dropdown(
            parent,
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

        self.fertilized = self.create_dropdown(
            parent,
            "Fertilized",
            3,
            [
                "Yes",
                "No"
            ]
        )

        self.weather_zone = self.create_dropdown(
            parent,
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

        self.seed_quality = self.create_dropdown(
            parent,
            "Seed Quality",
            5,
            [
                "High",
                "Medium",
                "Low"
            ]
        )

        self.irrigation_method = self.create_dropdown(
            parent,
            "Irrigation Method",
            6,
            [
                "Drip",
                "Sprinkler",
                "Flood",
                "Rainfed"
            ]
        )

        self.rainfall = self.create_entry(
            parent,
            "Rainfall (mm)",
            7,
            "120"
        )

        self.temperature = self.create_entry(
            parent,
            "Temperature (°C)",
            8,
            "27"
        )

        self.humidity = self.create_entry(
            parent,
            "Humidity (%)",
            9,
            "71"
        )

        self.soil_ph = self.create_entry(
            parent,
            "Soil pH",
            10,
            "6.5"
        )

        self.nitrogen = self.create_entry(
            parent,
            "Nitrogen (kg/ha)",
            11,
            "72"
        )

        self.phosphorus = self.create_entry(
            parent,
            "Phosphorus (kg/ha)",
            12,
            "45"
        )

        self.potassium = self.create_entry(
            parent,
            "Potassium (kg/ha)",
            13,
            "60"
        )

        self.irrigation = self.create_entry(
            parent,
            "Irrigation (mm)",
            14,
            "80"
        )

        self.harvest_days = self.create_entry(
            parent,
            "Days Since Harvest",
            15,
            "30"
        )

        self.pest_index = self.create_entry(
            parent,
            "Pest Index",
            16,
            "10"
        )

        upload_button = tk.Button(
            parent,
            text="UPLOAD LEAF IMAGE",
            command=self.upload_image,
            font=("Arial", 10, "bold"),
            width=27,
            height=2,
            cursor="hand2"
        )

        upload_button.grid(
            row=17,
            column=0,
            columnspan=2,
            pady=(15, 5)
        )

        self.image_status = tk.Label(
            parent,
            text="No image selected",
            bg="#FFFFFF",
            fg="#555555",
            wraplength=240,
            font=("Arial", 8)
        )

        self.image_status.grid(
            row=18,
            column=0,
            columnspan=2,
            pady=3
        )


    def create_entry(
        self,
        parent,
        label,
        row,
        default
    ):

        tk.Label(
            parent,
            text=label,
            bg="#FFFFFF",
            font=("Arial", 9),
            anchor="w"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=3
        )

        entry = tk.Entry(
            parent,
            width=18
        )

        entry.grid(
            row=row,
            column=1,
            padx=(8, 0),
            pady=3
        )

        entry.insert(
            0,
            default
        )

        return entry


    def create_dropdown(
        self,
        parent,
        label,
        row,
        values
    ):

        tk.Label(
            parent,
            text=label,
            bg="#FFFFFF",
            font=("Arial", 9),
            anchor="w"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=3
        )

        variable = tk.StringVar(
            value=values[0]
        )

        menu = tk.OptionMenu(
            parent,
            variable,
            *values
        )

        menu.config(
            width=15
        )

        menu.grid(
            row=row,
            column=1,
            padx=(8, 0),
            pady=3
        )

        return variable


    def create_right_panel(
        self,
        parent
    ):

        right = tk.Frame(
            parent,
            bg="#F3F6F4"
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_summary_cards(
            right
        )

        self.create_analysis_area(
            right
        )


    def create_summary_cards(
        self,
        parent
    ):

        cards = tk.Frame(
            parent,
            bg="#F3F6F4"
        )

        cards.pack(
            fill="x"
        )

        self.yield_card = self.create_card(
            cards,
            "CROP YIELD",
            "—"
        )

        self.disease_card = self.create_card(
            cards,
            "DISEASE",
            "—"
        )

        self.confidence_card = self.create_card(
            cards,
            "CONFIDENCE",
            "—"
        )

        self.health_card = self.create_card(
            cards,
            "HEALTH SCORE",
            "—"
        )

        self.risk_card = self.create_card(
            cards,
            "RISK",
            "—"
        )

        self.spectral_card = self.create_card(
            cards,
            "SPECTRAL STRESS",
            "—"
        )


    def create_card(
        self,
        parent,
        title,
        value
    ):

        frame = tk.Frame(
            parent,
            bg="#FFFFFF",
            bd=1,
            relief="solid"
        )

        frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=3
        )

        title_label = tk.Label(
            frame,
            text=title,
            font=("Arial", 8, "bold"),
            fg="#666666",
            bg="#FFFFFF"
        )

        title_label.pack(
            pady=(10, 2)
        )

        value_label = tk.Label(
            frame,
            text=value,
            font=("Arial", 13, "bold"),
            fg="#173F2F",
            bg="#FFFFFF"
        )

        value_label.pack(
            pady=(2, 10)
        )

        return value_label


    def create_analysis_area(
        self,
        parent
    ):

        area = tk.Frame(
            parent,
            bg="#F3F6F4"
        )

        area.pack(
            fill="both",
            expand=True,
            pady=(12, 0)
        )

        image_frame = tk.LabelFrame(
            area,
            text="LEAF IMAGE",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            padx=10,
            pady=10
        )

        image_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        image_content = tk.Frame(
            image_frame,
            bg="#FFFFFF"
        )

        image_content.pack(
            fill="both",
            expand=True
        )

        original_frame = tk.LabelFrame(
            image_content,
            text="ORIGINAL IMAGE",
            font=("Arial", 9, "bold"),
            bg="#FFFFFF",
            padx=5,
            pady=5
        )

        original_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 4)
        )

        self.image_display = tk.Label(
            original_frame,
            text="Upload a leaf image",
            font=("Arial", 11),
            bg="#FFFFFF",
            fg="#777777"
        )

        self.image_display.pack(
            fill="both",
            expand=True
        )

        visualization_frame = tk.LabelFrame(
            image_content,
            text="STRESS VISUALIZATION",
            font=("Arial", 9, "bold"),
            bg="#FFFFFF",
            padx=5,
            pady=5
        )

        visualization_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(4, 0)
        )

        self.visualization_display = tk.Label(
            visualization_frame,
            text="Stress map will appear here",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#777777"
        )

        self.visualization_display.pack(
            fill="both",
            expand=True
        )

        result_frame = tk.LabelFrame(
            area,
            text="AI ANALYSIS",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            padx=10,
            pady=10
        )

        result_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        self.result_text = tk.Text(
            result_frame,
            font=("Consolas", 9),
            bg="#FFFFFF",
            fg="#222222",
            wrap="word",
            relief="flat"
        )

        self.result_text.pack(
            fill="both",
            expand=True
        )

        self.show_initial_message()


    def show_initial_message(self):

        self.result_text.delete(
            "1.0",
            tk.END
        )

        self.result_text.insert(
            tk.END,
            "AGRIVISION AI\n"
        )

        self.result_text.insert(
            tk.END,
            "========================================\n\n"
        )

        self.result_text.insert(
            tk.END,
            "Upload a crop leaf image to begin.\n\n"
        )

        self.result_text.insert(
            tk.END,
            "The system will automatically run:\n\n"
        )

        self.result_text.insert(
            tk.END,
            "• Image Validation\n"
        )

        self.result_text.insert(
            tk.END,
            "• Yield Prediction\n"
        )

        self.result_text.insert(
            tk.END,
            "• Disease Detection\n"
        )

        self.result_text.insert(
            tk.END,
            "• Spectral Analysis\n"
        )

        self.result_text.insert(
            tk.END,
            "• Stress Heatmap Visualization\n"
        )

        self.result_text.insert(
            tk.END,
            "• Crop Health Scoring\n"
        )

        self.result_text.insert(
            tk.END,
            "• Risk Analysis\n"
        )

        self.result_text.insert(
            tk.END,
            "• Forecast Analysis\n"
        )

        self.result_text.insert(
            tk.END,
            "• AI Recommendations\n"
        )


    def create_status_bar(self):

        frame = tk.Frame(
            self.root,
            bg="#F3F6F4",
            height=35
        )

        frame.pack(
            fill="x",
            padx=18,
            pady=(0, 8)
        )

        frame.pack_propagate(
            False
        )

        self.status_label = tk.Label(
            frame,
            text="Ready — upload a leaf image",
            bg="#F3F6F4",
            fg="#555555",
            font=("Arial", 10, "bold")
        )

        self.status_label.pack(
            pady=7
        )


    def upload_image(self):

        path = filedialog.askopenfilename(
            title="Select Leaf Image",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.JPG *.JPEG *.PNG *.tif *.tiff *.TIF *.TIFF"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not path:
            return

        self.image_path = path

        self.image_status.config(
            text=os.path.basename(
                path
            )
        )

        try:

            image = Image.open(
                path
            )

            image.thumbnail(
                (500, 500)
            )

            self.preview_image = ImageTk.PhotoImage(
                image
            )

            self.image_display.config(
                image=self.preview_image,
                text=""
            )

            self.status_label.config(
                text="Image uploaded — validating image...",
                fg="#B26A00"
            )

            self.root.update()

            self.analyze()

        except Exception as error:

            messagebox.showerror(
                "Image Error",
                str(error)
            )

            self.status_label.config(
                text="Image loading failed",
                fg="#B00020"
            )


    def reset_cards(self):

        self.yield_card.config(
            text="—"
        )

        self.disease_card.config(
            text="—"
        )

        self.confidence_card.config(
            text="—"
        )

        self.health_card.config(
            text="—"
        )

        self.risk_card.config(
            text="—"
        )

        self.spectral_card.config(
            text="—"
        )

        self.visualization_image = None
        self.hyperleaf_result = None
        self.visualization_display.config(
            image="",
            text="Stress map will appear here"
        )


    def analyze(self):

        if not self.image_path:
            return

        try:

            self.result_text.delete(
                "1.0",
                tk.END
            )

            self.reset_cards()

            self.result_text.insert(
                tk.END,
                "AGRIVISION AI\n"
            )

            self.result_text.insert(
                tk.END,
                "========================================\n\n"
            )

            self.result_text.insert(
                tk.END,
                "VALIDATING IMAGE...\n\n"
            )

            self.root.update()

            validation_result = validate_crop_image(
                self.image_path
            )

            if not validation_result["valid"]:

                self.result_text.delete(
                    "1.0",
                    tk.END
                )

                self.result_text.insert(
                    tk.END,
                    "AGRIVISION AI\n"
                )

                self.result_text.insert(
                    tk.END,
                    "========================================\n\n"
                )

                self.result_text.insert(
                    tk.END,
                    "IMAGE VALIDATION FAILED\n\n"
                )

                self.result_text.insert(
                    tk.END,
                    "The uploaded image does not appear "
                    "to contain a crop or leaf.\n\n"
                )

                self.result_text.insert(
                    tk.END,
                    f"Reason: "
                    f"{validation_result['reason']}\n\n"
                )

                self.result_text.insert(
                    tk.END,
                    f"Green Ratio: "
                    f"{validation_result['green_ratio']:.2%}\n"
                )

                self.result_text.insert(
                    tk.END,
                    f"Vegetation Ratio: "
                    f"{validation_result['vegetation_ratio']:.2%}\n\n"
                )

                self.result_text.insert(
                    tk.END,
                    "Please upload a clear image of "
                    "a crop leaf.\n\n"
                )

                self.result_text.insert(
                    tk.END,
                    "Analysis stopped.\n"
                )

                self.status_label.config(
                    text="✗ Invalid crop image — analysis stopped",
                    fg="#B00020"
                )

                return

            self.result_text.insert(
                tk.END,
                "✓ Crop/vegetation image detected.\n"
            )

            self.result_text.insert(
                tk.END,
                f"Green Ratio: "
                f"{validation_result['green_ratio']:.2%}\n"
            )

            self.result_text.insert(
                tk.END,
                f"Vegetation Ratio: "
                f"{validation_result['vegetation_ratio']:.2%}\n\n"
            )

            self.result_text.insert(
                tk.END,
                "AI ANALYSIS IN PROGRESS...\n\n"
            )

            self.result_text.insert(
                tk.END,
                "Running yield prediction...\n"
            )

            self.root.update()

            yield_result = predict_crop_yield(

                rainfall_mm=float(
                    self.rainfall.get()
                ),

                avg_temp_c=float(
                    self.temperature.get()
                ),

                humidity_pct=float(
                    self.humidity.get()
                ),

                soil_ph=float(
                    self.soil_ph.get()
                ),

                nitrogen_kg_ha=float(
                    self.nitrogen.get()
                ),

                phosphorus_kg_ha=float(
                    self.phosphorus.get()
                ),

                potassium_kg_ha=float(
                    self.potassium.get()
                ),

                irrigation_mm=float(
                    self.irrigation.get()
                ),

                days_from_last_harvest=float(
                    self.harvest_days.get()
                ),

                pest_index=float(
                    self.pest_index.get()
                ),

                soil_type=self.soil_type.get(),

                crop_type=self.crop.get(),

                fertilized=self.fertilized.get(),

                weather_zone=self.weather_zone.get(),

                seed_quality=self.seed_quality.get(),

                irrigation_method=self.irrigation_method.get(),

                season=self.season.get()
            )

            self.result_text.insert(
                tk.END,
                "✓ Yield prediction completed.\n"
            )

            self.result_text.insert(
                tk.END,
                "Running disease detection...\n"
            )

            self.root.update()

            disease_result = predict_disease(
                self.image_path
            )

            self.result_text.insert(
                tk.END,
                "✓ Disease detection completed.\n"
            )

            self.run_hyperleaf_prediction()

            self.result_text.insert(
                tk.END,
                "Running spectral analysis...\n"
            )

            self.root.update()

            processed_image = preprocess_leaf_image(
                self.image_path
            )

            spectral_result = analyze_leaf_spectrum(
                processed_image
            )

            self.result_text.insert(
                tk.END,
                "✓ Spectral analysis completed.\n"
            )

            self.result_text.insert(
                tk.END,
                "Generating stress visualization...\n"
            )

            self.root.update()

            visualization_result = generate_stress_visualization(
                self.image_path
            )

            self.result_text.insert(
                tk.END,
                "✓ Stress visualization completed.\n"
            )

            self.display_stress_visualization(
                visualization_result
            )

            if isinstance(
                yield_result,
                dict
            ):

                yield_value = float(
                    yield_result[
                        "predicted_yield_tons_per_hectare"
                    ]
                )

                yield_crop = str(
                    yield_result[
                        "crop"
                    ]
                )

                yield_category = str(
                    yield_result[
                        "yield_category"
                    ]
                )

            else:

                yield_value = float(
                    yield_result
                )

                yield_crop = self.crop.get()

                if yield_value < 2:
                    yield_category = "Low"

                elif yield_value < 4:
                    yield_category = "Moderate"

                elif yield_value < 6:
                    yield_category = "Good"

                else:
                    yield_category = "High"

            detected_crop = str(
                disease_result[
                    "crop"
                ]
            )

            disease = str(
                disease_result[
                    "disease"
                ]
            )

            confidence = float(
                disease_result[
                    "confidence"
                ]
            )

            spectral_analysis = spectral_result[
                "analysis"
            ]

            spectral_stress = float(
                spectral_analysis[
                    "spectral_stress_score"
                ]
            )

            crop_match = (
                yield_crop.lower().strip()
                ==
                detected_crop.lower().strip()
            )

            self.result_text.insert(
                tk.END,
                "Calculating crop health...\n"
            )

            self.root.update()

            health_result = calculate_health_score(

                yield_value=yield_value,

                yield_category=yield_category,

                disease=disease,

                disease_confidence=confidence,

                crop_consistency=crop_match,

                pest_index=float(
                    self.pest_index.get()
                ),

                humidity_pct=float(
                    self.humidity.get()
                ),

                soil_ph=float(
                    self.soil_ph.get()
                ),

                spectral_stress=spectral_stress
            )

            health_score = float(
                health_result[
                    "health_score"
                ]
            )

            health_status = str(
                health_result[
                    "health_status"
                ]
            )

            self.result_text.insert(
                tk.END,
                "✓ Health score calculated.\n"
            )

            self.result_text.insert(
                tk.END,
                "Calculating risk...\n"
            )

            self.root.update()

            risk_result = calculate_risk(

                disease=disease,

                disease_confidence=confidence,

                yield_category=yield_category,

                pest_index=float(
                    self.pest_index.get()
                ),

                humidity_pct=float(
                    self.humidity.get()
                ),

                crop_consistency=crop_match,

                spectral_stress=spectral_stress
            )

            risk_score = float(
                risk_result[
                    "overall_risk_score"
                ]
            )

            risk_level = str(
                risk_result[
                    "risk_level"
                ]
            )

            self.result_text.insert(
                tk.END,
                "✓ Risk analysis completed.\n"
            )

            self.result_text.insert(
                tk.END,
                "Generating forecast...\n"
            )

            self.root.update()

            forecast_result = generate_forecast(

                current_yield=yield_value,

                yield_category=yield_category,

                disease_risk=risk_score,

                health_score=health_score,

                forecast_days=14
            )

            self.result_text.insert(
                tk.END,
                "✓ Forecast completed.\n"
            )

            self.result_text.insert(
                tk.END,
                "Generating recommendations...\n"
            )

            self.root.update()

            recommendation_result = (
                generate_recommendations(

                    crop=detected_crop,

                    disease=disease,

                    disease_confidence=confidence,

                    yield_category=yield_category,

                    health_score=health_score,

                    health_status=health_status,

                    risk_level=risk_level,

                    pest_index=float(
                        self.pest_index.get()
                    ),

                    humidity_pct=float(
                        self.humidity.get()
                    ),

                    soil_ph=float(
                        self.soil_ph.get()
                    ),

                    spectral_stress=spectral_stress
                )
            )

            self.update_cards(

                yield_value,

                disease,

                confidence,

                health_score,

                risk_level,

                spectral_stress
            )

            self.display_results(

                yield_crop=yield_crop,

                yield_value=yield_value,

                yield_category=yield_category,

                detected_crop=detected_crop,

                disease=disease,

                confidence=confidence,

                disease_result=disease_result,

                health_result=health_result,

                risk_result=risk_result,

                forecast_result=forecast_result,

                recommendation_result=recommendation_result,

                spectral_result=spectral_result,

                visualization_result=visualization_result,

                crop_match=crop_match
            )

            self.status_label.config(
                text="✓ Complete AI analysis finished",
                fg="#246B45"
            )

        except ValueError as error:

            messagebox.showerror(
                "Invalid Input",
                str(error)
            )

            self.status_label.config(
                text="Invalid farm input",
                fg="#B00020"
            )

        except Exception as error:

            messagebox.showerror(
                "Analysis Error",
                str(error)
            )

            self.status_label.config(
                text="Analysis failed",
                fg="#B00020"
            )


    def run_hyperleaf_prediction(self):

        """Run trained HyperLeaf model when a hyperspectral TIFF is uploaded."""

        self.hyperleaf_result = None

        if not self.image_path:
            return None

        extension = os.path.splitext(
            self.image_path
        )[1].lower()

        if extension not in (".tif", ".tiff"):
            return None

        self.result_text.insert(
            tk.END,
            "Running trained HyperLeaf spectral model...\n"
        )
        self.root.update()

        result = predict_spectral(
            self.image_path
        )

        self.hyperleaf_result = result

        self.result_text.insert(
            tk.END,
            "✓ HyperLeaf spectral prediction completed.\n"
        )

        return result


    def display_stress_visualization(
        self,
        visualization_result
    ):

        marked_path = visualization_result.get(
            "marked_path"
        )

        if not marked_path or not os.path.exists(
            marked_path
        ):
            return

        image = Image.open(
            marked_path
        ).convert("RGB")

        image.thumbnail(
            (500, 500)
        )

        self.visualization_image = ImageTk.PhotoImage(
            image
        )

        self.visualization_display.config(
            image=self.visualization_image,
            text=""
        )


    def update_cards(
        self,
        yield_value,
        disease,
        confidence,
        health_score,
        risk_level,
        spectral_stress
    ):

        self.yield_card.config(
            text=f"{yield_value:.2f} t/ha"
        )

        disease_display = disease.replace(
            "___",
            " - "
        )

        self.disease_card.config(
            text=disease_display[:22]
        )

        self.confidence_card.config(
            text=f"{confidence:.1f}%"
        )

        self.health_card.config(
            text=f"{health_score:.0f}/100"
        )

        self.risk_card.config(
            text=risk_level
        )

        self.spectral_card.config(
            text=f"{spectral_stress:.0f}/100"
        )


    def display_results(
        self,
        yield_crop,
        yield_value,
        yield_category,
        detected_crop,
        disease,
        confidence,
        disease_result,
        health_result,
        risk_result,
        forecast_result,
        recommendation_result,
        spectral_result,
        visualization_result,
        crop_match
    ):

        self.result_text.delete(
            "1.0",
            tk.END
        )

        spectral_analysis = spectral_result[
            "analysis"
        ]

        self.result_text.insert(
            tk.END,
            "AGRIVISION AI — COMPLETE ANALYSIS\n"
        )

        self.result_text.insert(
            tk.END,
            "========================================\n\n"
        )

        self.result_text.insert(
            tk.END,
            "IMAGE VALIDATION\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            "Status             : VERIFIED\n\n"
        )

        self.result_text.insert(
            tk.END,
            "CROP INTELLIGENCE\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            f"Farm Crop          : {yield_crop}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Predicted Yield    : "
            f"{yield_value:.3f} tons/hectare\n"
        )

        self.result_text.insert(
            tk.END,
            f"Yield Category     : "
            f"{yield_category}\n\n"
        )

        self.result_text.insert(
            tk.END,
            "DISEASE INTELLIGENCE\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            f"Detected Crop      : "
            f"{detected_crop}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Disease            : "
            f"{disease}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Confidence         : "
            f"{confidence:.2f}%\n"
        )

        self.result_text.insert(
            tk.END,
            f"Status             : "
            f"{disease_result['status']}\n\n"
        )

        self.result_text.insert(
            tk.END,
            "SPECTRAL INTELLIGENCE\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            f"Spectral Stress    : "
            f"{spectral_analysis['spectral_stress_score']:.1f}/100\n"
        )

        self.result_text.insert(
            tk.END,
            f"Stress Level       : "
            f"{spectral_analysis['stress_level']}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Vegetation State   : "
            f"{spectral_analysis['vegetation_condition']}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Discoloration      : "
            f"{spectral_analysis['discoloration_level']}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Tissue Damage      : "
            f"{spectral_analysis['tissue_damage_level']}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Vegetation Index   : "
            f"{spectral_analysis['vegetation_index']:.4f}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Excess Green Index : "
            f"{spectral_analysis['excess_green_index']:.2f}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Green Ratio        : "
            f"{spectral_analysis['green_ratio']:.4f}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Saturation         : "
            f"{spectral_analysis['saturation']:.2f}\n\n"
        )

        if self.hyperleaf_result:

            self.result_text.insert(
                tk.END,
                "TRAINED HYPERLEAF MODEL\n"
            )

            self.result_text.insert(
                tk.END,
                "----------------------------------------\n"
            )

            self.result_text.insert(
                tk.END,
                f"Spectral Bands     : "
                f"{self.hyperleaf_result['spectral_bands']}\n"
            )

            self.result_text.insert(
                tk.END,
                f"Grain Weight       : "
                f"{self.hyperleaf_result['grain_weight']:.4f}\n"
            )

            self.result_text.insert(
                tk.END,
                f"Gsw                : "
                f"{self.hyperleaf_result['gsw']:.6f}\n"
            )

            self.result_text.insert(
                tk.END,
                f"PhiPS2             : "
                f"{self.hyperleaf_result['phi_ps2']:.6f}\n\n"
            )

        self.result_text.insert(
            tk.END,
            "STRESS VISUALIZATION\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            f"Average Stress      : "
            f"{visualization_result['average_stress']:.2f}/100\n"
        )

        self.result_text.insert(
            tk.END,
            f"Stress Level        : "
            f"{visualization_result['stress_level']}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Affected Leaf Area  : "
            f"{visualization_result['affected_area_percentage']:.2f}%\n"
        )

        self.result_text.insert(
            tk.END,
            f"Stressed Regions    : "
            f"{visualization_result['num_stressed_regions']}\n\n"
        )

        self.result_text.insert(
            tk.END,
            "CROP HEALTH\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            f"Health Score       : "
            f"{health_result['health_score']:.0f}/100\n"
        )

        self.result_text.insert(
            tk.END,
            f"Health Status      : "
            f"{health_result['health_status']}\n\n"
        )

        self.result_text.insert(
            tk.END,
            "RISK ANALYSIS\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            f"Overall Risk       : "
            f"{risk_result['overall_risk_score']:.1f}/100\n"
        )

        self.result_text.insert(
            tk.END,
            f"Risk Level         : "
            f"{risk_result['risk_level']}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Disease Risk       : "
            f"{risk_result['disease_risk']:.1f}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Pest Risk          : "
            f"{risk_result['pest_risk']:.1f}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Environmental Risk : "
            f"{risk_result['environmental_risk']:.1f}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Yield Risk         : "
            f"{risk_result['yield_risk']:.1f}\n\n"
        )

        self.result_text.insert(
            tk.END,
            "FORECAST\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        self.result_text.insert(
            tk.END,
            f"Forecast Period    : "
            f"{forecast_result['forecast_days']} days\n"
        )

        self.result_text.insert(
            tk.END,
            f"Current Yield      : "
            f"{forecast_result['current_yield']:.3f} t/ha\n"
        )

        self.result_text.insert(
            tk.END,
            f"Projected Yield    : "
            f"{forecast_result['projected_yield']:.3f} t/ha\n"
        )

        self.result_text.insert(
            tk.END,
            f"Future Disease Risk: "
            f"{forecast_result['projected_disease_risk']:.1f}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Future Risk Level  : "
            f"{forecast_result['future_risk_level']}\n"
        )

        self.result_text.insert(
            tk.END,
            f"Forecast Type      : "
            f"{forecast_result['forecast_type']}\n\n"
        )

        self.result_text.insert(
            tk.END,
            "CROP CONSISTENCY\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        if crop_match:

            self.result_text.insert(
                tk.END,
                "Status             : VERIFIED\n\n"
            )

        else:

            self.result_text.insert(
                tk.END,
                "Status             : WARNING\n"
            )

            self.result_text.insert(
                tk.END,
                f"Farm Crop          : "
                f"{yield_crop}\n"
            )

            self.result_text.insert(
                tk.END,
                f"Detected Crop      : "
                f"{detected_crop}\n\n"
            )

        self.result_text.insert(
            tk.END,
            "TOP 3 DISEASE PREDICTIONS\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        for index, prediction in enumerate(
            disease_result[
                "top_predictions"
            ],
            start=1
        ):

            self.result_text.insert(
                tk.END,
                f"{index}. "
                f"{prediction['class']} - "
                f"{prediction['confidence']:.2f}%\n"
            )

        self.result_text.insert(
            tk.END,
            "\nRECOMMENDATIONS\n"
        )

        self.result_text.insert(
            tk.END,
            "----------------------------------------\n"
        )

        priority_areas = (
            recommendation_result[
                "priority_areas"
            ]
        )

        if priority_areas:

            self.result_text.insert(
                tk.END,
                "Priority Areas:\n"
            )

            for priority in priority_areas:

                self.result_text.insert(
                    tk.END,
                    f"• {priority}\n"
                )

            self.result_text.insert(
                tk.END,
                "\n"
            )

        for recommendation in (
            recommendation_result[
                "recommendations"
            ]
        ):

            self.result_text.insert(
                tk.END,
                f"• {recommendation}\n"
            )

        self.result_text.insert(
            tk.END,
            "\n========================================\n"
        )

        self.result_text.insert(
            tk.END,
            "ANALYSIS COMPLETED\n"
        )

        self.result_text.insert(
            tk.END,
            "========================================\n"
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = AgriVisionDashboard(
        root
    )

    root.mainloop()