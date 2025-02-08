import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_reader import DataReader
from metadata_loader import MetadataLoader
import pandas as pd
import matplotlib.ticker as mticker
import webbrowser
from ui.date_selector import DateSelector
import tkinter.filedialog



class MainScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data_reader = DataReader("data.xlsx")
        self.metadata_loader = MetadataLoader("indicators_mapping.json")

        self.selected_indicator = None
        self.selected_country = None
        self.chart_canvas = None

        self.configure_layout()
        self.populate_indicators()

    def configure_layout(self):
        #Configures the UI layout
        self.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=3)  #Chart 70%
        self.columnconfigure(1, weight=1)  #Data 30%

        #Top Controls Row (Dropdown & Country Buttons)
        self.top_controls_frame = ctk.CTkFrame(self, height=50)
        self.top_controls_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        self.top_controls_frame.columnconfigure(0, weight=1)

        #Indicator Dropdown (Left Side)
        self.indicator_menu = ctk.CTkOptionMenu(self.top_controls_frame, values=["Choose Indicator"], command=self.on_indicator_selected)
        self.indicator_menu.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        #Country Buttons Frame (To the Right of Dropdown)
        self.country_buttons_frame = ctk.CTkFrame(self.top_controls_frame)
        self.country_buttons_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.country_buttons_frame.grid_remove()  # Hide initially
        self.country_buttons = {}

        #Main Display Layout (Chart & Data Side by Side)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=3)  #Chart 70%
        self.main_frame.columnconfigure(1, weight=1)  #Data 30%
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.grid_remove()  #Hide everything at startup

        #Chart Frame (Left Side)
        self.chart_frame = ctk.CTkFrame(self.main_frame, corner_radius=8)
        self.chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Data Display (Right Side)
        self.data_display = ctk.CTkFrame(self.main_frame, corner_radius=8, width=350)
        self.data_display.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        #Title Label
        self.title_label = ctk.CTkLabel(self.data_display, text="Choose Indicator", font=("Arial", 22, "bold"), anchor="center", wraplength=300)
        self.title_label.pack(pady=5)

        #Impact Label
        self.impact_label = ctk.CTkLabel(self.data_display, text="", font=("Arial", 18, "bold"))
        self.impact_label.pack(pady=10)

        #Data Box (With Values & Buttons)
        self.data_box = ctk.CTkFrame(self.data_display, width=300, height=180, corner_radius=8)
        self.data_box.pack_propagate(False)
        self.data_box.pack(pady=10, padx=10)

        self.date_label = ctk.CTkLabel(self.data_box, text="Date: ", font=("Arial", 14, "bold"))
        self.date_label.pack(pady=2)

        self.actual_label = ctk.CTkLabel(self.data_box, text="Actual: ", font=("Arial", 14))
        self.actual_label.pack()

        self.forecast_label = ctk.CTkLabel(self.data_box, text="Forecast: ", font=("Arial", 14))
        self.forecast_label.pack()

        self.previous_label = ctk.CTkLabel(self.data_box, text="Previous: ", font=("Arial", 14))
        self.previous_label.pack()

        #Buttons Inside `data_box`
        self.button_frame = ctk.CTkFrame(self.data_box)  #Frame for button alignment
        self.button_frame.pack(pady=5)

        self.source_button = ctk.CTkButton(self.button_frame, text="Source", command=self.open_source, width=120)
        self.source_button.pack(side="left", padx=5)

        self.by_date_button = ctk.CTkButton(self.button_frame, text="By Date", command=self.open_date_selector, width=120)
        self.by_date_button.pack(side="right", padx=5)

        self.export_chart_button = ctk.CTkButton(self.data_box, text="Export Chart", command=self.export_chart, width=150)
        self.export_chart_button.pack(pady=5)

        #Metadata Box
        self.data_label = ctk.CTkTextbox(self.data_display, wrap="word", height=150)
        self.data_label.pack(fill="both", expand=True, padx=10, pady=10)

    def open_source(self):
        #Opens the source link from metadata in the default browser
        if not self.selected_indicator or not self.selected_country:
            return  #Exit if no selection

        #Retrieve metadata for the selected indicator and country
        metadata = self.metadata_loader.get_metadata(self.selected_indicator, self.selected_country)

        #Extract source URL
        source_url = metadata.get("source", "").strip()

        if source_url:
            webbrowser.open(source_url)


    def open_date_selector(self):
        #Opens the date selection window
        if self.selected_indicator and self.selected_country:
            DateSelector(self.selected_indicator, self.selected_country, self.data_reader)


    def populate_indicators(self):
        #Loads indicators dynamically from the Excel file
        indicators = self.data_reader.get_available_indicators()
        self.indicator_menu.configure(values=indicators)

    def on_indicator_selected(self, indicator):
        #Handles indicator selection, showing UI elements when an indicator is chosen
        self.selected_indicator = indicator.strip().upper()

        #While "Choose Indicator", keep everything hidden
        if self.selected_indicator == "CHOOSE INDICATOR":
            self.country_buttons_frame.grid_remove()
            self.main_frame.grid_remove()  #Keep main UI hidden
            return

        self.title_label.configure(text=self.selected_indicator)

        countries = self.data_reader.get_available_countries(indicator)

        #Clear previous buttons
        for widget in self.country_buttons_frame.winfo_children():
            widget.destroy()
        self.country_buttons.clear()

        #Hide country buttons frame if no countries exist
        if not countries:
            self.country_buttons_frame.grid_remove()
            return

        #Create country buttons
        for country in countries:
            btn = ctk.CTkButton(self.country_buttons_frame, text=country,
                                command=lambda c=country: self.on_country_selected(c), fg_color="gray")
            btn.pack(side="left", padx=5, pady=5)
            self.country_buttons[country] = btn

        self.country_buttons_frame.grid()

        #Show UI elements when an indicator is selected
        self.main_frame.grid()

    def on_country_selected(self, country):
        #Handles country selection and updates UI with data
        self.selected_country = country.upper()

        #Reset button colors
        for btn_country, btn in self.country_buttons.items():
            btn.configure(fg_color="gray")

        if country in self.country_buttons:
            self.country_buttons[country].configure(fg_color="#1E90FF")

        data = self.data_reader.get_latest_data(self.selected_indicator, self.selected_country)
        metadata = self.metadata_loader.get_metadata(self.selected_indicator, self.selected_country)

        if not data or not metadata:
            return

        #Update Data Labels
        self.date_label.configure(text=f"Date: {data.get('date', 'N/A')}")
        self.actual_label.configure(text=f"Actual: {self.clean_number_display(data.get('actual', 'N/A'))}")
        self.forecast_label.configure(text=f"Forecast: {self.clean_number_display(data.get('forecast', 'N/A'))}")
        self.previous_label.configure(text=f"Previous: {self.clean_number_display(data.get('previous', 'N/A'))}")

        #Impact Label Coloring
        impact = metadata.get("impact", "N/A").strip().lower()
        impact_color = self.get_impact_color(impact)
        self.impact_label.configure(text=f"⚠️ Impact: {metadata.get('impact', 'N/A')}", text_color=impact_color)

        #Metadata Display
        display_text = f"Description: {metadata.get('description', 'N/A')}\n" \
                       "\n" \
                       f"Derived Via: {metadata.get('derived_via', 'N/A')}\n" \
                       "\n" \
                       f"Acronym: {metadata.get('acro', 'N/A')}\n" \
                       "\n" \
                       f"Event Type: {metadata.get('event_type', 'N/A')}\n" \
                       "\n" \
                       f"Frequency: {metadata.get('frequency', 'N/A')}\n" \
                       "\n" \
                       f"Usual Effect: {metadata.get('usual_effect', 'N/A')}"

        self.data_label.delete("1.0", "end")
        self.data_label.insert("1.0", display_text)

        #Display Chart
        self.display_chart()

    def display_chart(self):
        #Displays the historical data chart with fixed vertical axis labels
        data = self.data_reader.get_historical_data(self.selected_indicator, self.selected_country)

        if data is None or data.empty:

            return


        #Convert 'DATE' column to datetime format
        data["DATE"] = pd.to_datetime(data["DATE"], errors="coerce")  # Convert to datetime
        data = data.dropna(subset=["DATE"])  # Remove invalid dates

        #Clean the 'ACTUAL' values: remove non-numeric characters and detect type
        is_percentage = False
        is_billions = False

        def clean_numeric(value):
            #Cleans numeric values and detects their type
            nonlocal is_percentage, is_billions

            try:
                if isinstance(value, str):
                    value = value.strip()

                    if value.endswith("%"):  #Detect percentage-based indicator
                        is_percentage = True
                        return float(value.replace("%", ""))

                    if value.endswith("B"):  #Convert billions (B) to actual numbers
                        is_billions = True
                        return float(value.replace("B", "")) * 1e9

                return float(value)  #Convert normally
            except ValueError:
                return None  #Convert invalid values to None

        data["ACTUAL"] = data["ACTUAL"].apply(clean_numeric)  #Apply cleaning function
        data = data.dropna(subset=["ACTUAL"])  #Remove rows with invalid numbers


        if data.empty:
            return  #No valid numerical data to plot

        fig, ax = plt.subplots(figsize=(10, 6))

        #Set min/max limits and create 10 evenly spaced y-ticks
        y_min, y_max = data["ACTUAL"].min(), data["ACTUAL"].max()

        if y_min == y_max:  #Prevent division by zero if all values are the same
            y_min -= 1
            y_max += 1

        y_ticks = np.linspace(y_min, y_max, 10)

        #Plot the data
        ax.plot(data["DATE"], data["ACTUAL"], marker="o", linestyle="-", color="blue", label="Actual Value")

        #Select 20 evenly spaced x-axis labels
        min_date, max_date = data["DATE"].min(), data["DATE"].max()
        x_ticks = pd.date_range(start=min_date, end=max_date, periods=20)  #20 evenly spaced points

        #Convert x-axis labels to YYYY-MM format
        x_labels = [date.strftime("%Y-%m") for date in x_ticks]

        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, rotation=45, ha="right")  #Rotate labels for readability

        ax.set_yticks(y_ticks)
        ax.set_title(f"{self.selected_indicator} Trends ({self.selected_country})", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date (YYYY-MM)", fontsize=12)

        #Dynamic Y-Axis Label Formatting
        if is_billions:
            ax.set_ylabel("Actual Value (Billions)", fontsize=12)

            def format_billions(x, _):
                return f"{x / 1e9:.1f}B"

            ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_billions))

        elif is_percentage:
            ax.set_ylabel("Actual Value (%)", fontsize=12)

            def format_percentage(x, _):
                return f"{x:.1f}%"

            ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_percentage))

        else:
            ax.set_ylabel("Actual Value", fontsize=12)  #Default for simple numbers

        ax.grid(True)
        ax.legend()

        #Destroy previous chart before creating a new one
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)


    def export_chart(self):
        #Exports the currently displayed chart as an image file
        if not self.chart_canvas:
            return

        #Ask user where to save the file
        file_path = tkinter.filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("PDF Document", "*.pdf")],
            title="Save Chart As"
        )

        if not file_path:  #User canceled the save dialog
            return

        #Save the chart as an image
        self.chart_canvas.figure.savefig(file_path, dpi=300)

    @staticmethod
    def clean_number_display(value):
        try:
            num = round(float(value), 6)
            return f"{num}".rstrip('0').rstrip('.')
        except (ValueError, TypeError):
            return value

    @staticmethod
    def get_impact_color(impact):
        impact_keywords = {"high": "red", "medium": "yellow", "low": "green"}
        for keyword, color in impact_keywords.items():
            if keyword in impact:
                return color
        return "gray"
