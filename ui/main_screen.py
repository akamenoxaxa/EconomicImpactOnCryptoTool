import customtkinter as ctk
from data_reader import DataReader
from metadata_loader import MetadataLoader
from ui.historical_data_screen import HistoricalDataScreen
import webbrowser


class MainScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data_reader = DataReader("data.xlsx")
        self.metadata_loader = MetadataLoader("indicators_mapping.json")

        self.selected_indicator = None
        self.selected_country = None
        self.source_url = ""

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

        # **Main Display Box (Below Country Buttons)**
        self.main_display_box = ctk.CTkFrame(self, width=700, height=400, corner_radius=8)
        self.main_display_box.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.main_display_box.grid_remove()

        # **Title (Centered in Main Display)**
        self.title_label = ctk.CTkLabel(self.main_display_box, text="Choose Indicator", font=("Arial", 22, "bold"), anchor="center")
        self.title_label.pack(pady=5)

        # **Mini Data Box (Inside Main Display)**
        self.data_box = ctk.CTkFrame(self.main_display_box, width=300, height=180, corner_radius=8)
        self.data_box.pack(pady=5, padx=10, anchor="center")
        self.data_box.pack_forget()

        self.date_label = ctk.CTkLabel(self.data_box, text="Date: ", font=("Arial", 14, "bold"))
        self.date_label.pack(pady=2)

        # Small box for displaying values
        self.values_frame = ctk.CTkFrame(self.data_box, width=250, height=100, corner_radius=8)
        self.values_frame.pack(pady=5)

        self.actual_label = ctk.CTkLabel(self.values_frame, text="Actual: ", font=("Arial", 14))
        self.actual_label.pack()

        self.forecast_label = ctk.CTkLabel(self.values_frame, text="Forecast: ", font=("Arial", 14))
        self.forecast_label.pack()

        self.previous_label = ctk.CTkLabel(self.values_frame, text="Previous: ", font=("Arial", 14))
        self.previous_label.pack()

        # **Metadata Box**
        self.data_label = ctk.CTkTextbox(self.main_display_box, wrap="word", width=600, height=200)
        self.data_label.pack(pady=10)

        # **Chart Button (Below Data Box)**
        self.chart_button = ctk.CTkButton(self.main_display_box, text="View Historical Chart", command=self.open_chart, state="disabled")
        self.chart_button.pack(pady=20)  # Increased padding for better spacing
        self.chart_button.pack_forget()

    def populate_indicators(self):
        """Loads indicators dynamically from the Excel file."""
        indicators = self.data_reader.get_available_indicators()
        self.indicator_menu.configure(values=indicators)

    def on_indicator_selected(self, indicator):
        """Handles indicator selection and creates country buttons dynamically."""
        self.selected_indicator = indicator.strip().upper()
        self.title_label.configure(text=self.selected_indicator)  # Update title when an indicator is chosen
        countries = self.data_reader.get_available_countries(indicator)

        # Clear previous buttons
        for widget in self.country_buttons_frame.winfo_children():
            widget.destroy()
        self.country_buttons.clear()

        # Create buttons for each country
        for country in countries:
            btn = ctk.CTkButton(self.country_buttons_frame, text=country, command=lambda c=country: self.on_country_selected(c), fg_color="gray")
            btn.pack(side="left", padx=5, pady=5)
            self.country_buttons[country] = btn

        self.country_buttons_frame.grid()
        self.main_display_box.grid_remove()

    def on_country_selected(self, country):
        """Handles country selection and updates UI with data."""
        self.selected_country = country.upper()

        # Reset button colors
        for btn_country, btn in self.country_buttons.items():
            btn.configure(fg_color="gray")

        if country in self.country_buttons:
            self.country_buttons[country].configure(fg_color="#1E90FF")  # UI blue

        data = self.data_reader.get_latest_data(self.selected_indicator, self.selected_country)
        metadata = self.metadata_loader.get_metadata(self.selected_indicator, self.selected_country)

        if not data or not metadata:
            self.main_display_box.grid_remove()
            return

        # Ensure all data values exist, otherwise default to "N/A"
        self.date_label.configure(text=f"Date: {data.get('date', 'N/A')}")
        self.actual_label.configure(text=f"Actual: {self.format_display_value(data.get('actual', 'N/A'))}")
        self.forecast_label.configure(text=f"Forecast: {self.format_display_value(data.get('forecast', 'N/A'))}")
        self.previous_label.configure(text=f"Previous: {self.format_display_value(data.get('previous', 'N/A'))}")

        # Display metadata
        display_text = f"🔹 **Description:** {metadata.get('description', 'N/A')}\n" \
                       f"🔹 **Derived Via:** {metadata.get('derived_via', 'N/A')}\n" \
                       f"🔹 **Acronym:** {metadata.get('acro', 'N/A')}\n" \
                       f"🔹 **Event Type:** {metadata.get('event_type', 'N/A')}\n" \
                       f"🔹 **Frequency:** {metadata.get('frequency', 'N/A')}\n" \
                       f"🔹 **Usual Effect:** {metadata.get('usual_effect', 'N/A')}\n" \
                       f"🔹 **Impact:** {metadata.get('impact', 'N/A')}"

        self.data_label.delete("1.0", "end")
        self.data_label.insert("1.0", display_text)

        self.main_display_box.grid()
        self.data_box.pack()  # Ensure data box is visible
        self.chart_button.configure(state="normal")
        self.chart_button.pack()

    @staticmethod
    def format_display_value(value):
        """Formats values to ensure percentages and large numbers display correctly."""
        try:
            if isinstance(value, str):
                value = value.replace(",", "").strip()

                # Handle billions (B) and millions (M)
                if value.endswith("B"):
                    return f"{float(value.replace('B', '')):.2f}B"
                elif value.endswith("M"):
                    return f"{float(value.replace('M', '')):.2f}M"

                # Handle percentage values
                if "%" in value or "<" in value or ">" in value:
                    value = value.replace("<", "").replace(">", "").replace("%", "").strip()
                    return f"{float(value):.2f}%"

            # Ensure decimal percentages are displayed correctly
            float_value = float(value)
            if 0 <= float_value < 1:  # Convert decimal percentages (e.g., 0.005 → 0.50%)
                return f"{float_value * 100:.2f}%"
            return f"{float_value:.2f}"
        except (ValueError, TypeError):
            return "N/A"

    def open_chart(self):
        """Opens historical data window."""
        if self.selected_indicator and self.selected_country:
            HistoricalDataScreen(self.selected_indicator, self.selected_country)
