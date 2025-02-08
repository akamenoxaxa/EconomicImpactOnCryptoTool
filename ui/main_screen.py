import customtkinter as ctk
from data_reader import DataReader
from metadata_loader import MetadataLoader
from ui.historical_data_screen import HistoricalDataScreen


class MainScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data_reader = DataReader("data.xlsx")
        self.metadata_loader = MetadataLoader("indicators_mapping.json")

        self.selected_indicator = None
        self.selected_country = None

        self.configure_layout()
        self.populate_indicators()

    def configure_layout(self):
        """Configures the UI layout properly without conflicts."""
        self.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)

        # **Indicator Dropdown**
        self.indicator_menu = ctk.CTkOptionMenu(self, values=["Choose Indicator"], command=self.on_indicator_selected)
        self.indicator_menu.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        # **Country Buttons Frame**
        self.country_buttons_frame = ctk.CTkFrame(self)
        self.country_buttons_frame.grid(row=1, column=0, padx=20, pady=5, sticky="n")
        self.country_buttons_frame.grid_remove()
        self.country_buttons = {}

        # **Main Display Box**
        self.main_display_box = ctk.CTkFrame(self, width=700, height=450, corner_radius=8)
        self.main_display_box.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.main_display_box.grid_remove()

        # **Title**
        self.title_label = ctk.CTkLabel(self.main_display_box, text="Choose Indicator", font=("Arial", 22, "bold"), anchor="center")
        self.title_label.pack(pady=5)

        # **Impact Label (Colored)**
        self.impact_label = ctk.CTkLabel(self.main_display_box, text="", font=("Arial", 20, "bold"))
        self.impact_label.pack(pady=10, padx=15, anchor="w")

        # **Data Box**
        self.data_box = ctk.CTkFrame(self.main_display_box, width=350, height=200, corner_radius=8)
        self.data_box.pack(pady=5, padx=10, anchor="center")
        self.data_box.pack_forget()

        self.date_label = ctk.CTkLabel(self.data_box, text="Date: ", font=("Arial", 14, "bold"))
        self.date_label.pack(pady=2)

        # **Expanded Values Box**
        self.values_frame = ctk.CTkFrame(self.data_box, width=300, height=130, corner_radius=8)
        self.values_frame.pack(pady=10)

        self.actual_label = ctk.CTkLabel(self.values_frame, text="Actual: ", font=("Arial", 14))
        self.actual_label.pack()

        self.forecast_label = ctk.CTkLabel(self.values_frame, text="Forecast: ", font=("Arial", 14))
        self.forecast_label.pack()

        self.previous_label = ctk.CTkLabel(self.values_frame, text="Previous: ", font=("Arial", 14))
        self.previous_label.pack()

        # **Metadata Box (Impact Removed)**
        self.data_label = ctk.CTkTextbox(self.main_display_box, wrap="word", width=600, height=200)
        self.data_label.pack(pady=10)

        # **Chart Button**
        self.chart_button = ctk.CTkButton(self.main_display_box, text="View Historical Chart", command=self.open_chart, state="disabled")
        self.chart_button.pack(pady=30)
        self.chart_button.pack_forget()

    def populate_indicators(self):
        """Loads indicators dynamically from the Excel file."""
        indicators = self.data_reader.get_available_indicators()
        self.indicator_menu.configure(values=indicators)

    def on_indicator_selected(self, indicator):
        """Handles indicator selection and creates country buttons dynamically."""
        self.selected_indicator = indicator.strip().upper()
        self.title_label.configure(text=self.selected_indicator)
        countries = self.data_reader.get_available_countries(indicator)

        for widget in self.country_buttons_frame.winfo_children():
            widget.destroy()
        self.country_buttons.clear()

        for country in countries:
            btn = ctk.CTkButton(self.country_buttons_frame, text=country, command=lambda c=country: self.on_country_selected(c), fg_color="gray")
            btn.pack(side="left", padx=5, pady=5)
            self.country_buttons[country] = btn

        self.country_buttons_frame.grid()
        self.main_display_box.grid_remove()

    def on_country_selected(self, country):
        """Handles country selection and updates UI with data."""
        self.selected_country = country.upper()

        for btn_country, btn in self.country_buttons.items():
            btn.configure(fg_color="gray")

        if country in self.country_buttons:
            self.country_buttons[country].configure(fg_color="#1E90FF")

        data = self.data_reader.get_latest_data(self.selected_indicator, self.selected_country)
        metadata = self.metadata_loader.get_metadata(self.selected_indicator, self.selected_country)

        if not data or not metadata:
            self.main_display_box.grid_remove()
            return

        # **Fix Floating-Point Precision Issue**
        self.date_label.configure(text=f"Date: {data.get('date', 'N/A')}")
        self.actual_label.configure(text=f"Actual: {self.clean_number_display(data.get('actual', 'N/A'))}")
        self.forecast_label.configure(text=f"Forecast: {self.clean_number_display(data.get('forecast', 'N/A'))}")
        self.previous_label.configure(text=f"Previous: {self.clean_number_display(data.get('previous', 'N/A'))}")

        # **Impact Label Coloring Fix**
        impact = metadata.get("impact", "N/A").strip().lower()
        impact_color = self.get_impact_color(impact)
        self.impact_label.configure(text=f"⚠️ Impact: {metadata.get('impact', 'N/A')}", text_color=impact_color)

        display_text = f"📌 **Description:** {metadata.get('description', 'N/A')}\n" \
                       f"📖 **Derived Via:** {metadata.get('derived_via', 'N/A')}\n" \
                       f"🔠 **Acronym:** {metadata.get('acro', 'N/A')}\n" \
                       f"📅 **Event Type:** {metadata.get('event_type', 'N/A')}\n" \
                       f"⏳ **Frequency:** {metadata.get('frequency', 'N/A')}\n" \
                       f"📊 **Usual Effect:** {metadata.get('usual_effect', 'N/A')}"

        self.data_label.delete("1.0", "end")
        self.data_label.insert("1.0", display_text)

        self.main_display_box.grid()
        self.data_box.pack()
        self.chart_button.configure(state="normal")
        self.chart_button.pack()

    def open_chart(self):
        """Opens historical data window."""
        if self.selected_indicator and self.selected_country:
            HistoricalDataScreen(self.selected_indicator, self.selected_country)

    @staticmethod
    def clean_number_display(value):
        """Fixes floating-point precision issues."""
        try:
            num = round(float(value), 6)  # Rounds to 6 decimal places max
            return f"{num}".rstrip('0').rstrip('.')  # Removes trailing zeros
        except (ValueError, TypeError):
            return value

    @staticmethod
    def get_impact_color(impact):
        """Fixes impact label color for multi-word values (e.g., High/Medium)."""
        impact_keywords = {"high": "red", "medium": "yellow", "low": "green"}
        for keyword, color in impact_keywords.items():
            if keyword in impact:
                return color
        return "gray"
