import customtkinter as ctk
from reading import Reading
from mappings import Mappings

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.reading = Reading("data.xlsx")
        self.mappings = Mappings("indicators_mapping.json")
        self.selected_country = None
        self.selected_indicator = None

        # UI Configuration
        self.grid_columnconfigure(0, weight=1)  # Left: Country and Indicators
        self.grid_columnconfigure(1, weight=2)  # Middle: Historical Data
        self.grid_columnconfigure(2, weight=3)  # Right: Calendar

        # Left: Country and Indicator Selection
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Country Selection
        self.country_label = ctk.CTkLabel(self.left_frame, text="Choose Country", font=("Arial", 16))
        self.country_label.pack(pady=10)

        self.country_dropdown = ctk.CTkOptionMenu(
            self.left_frame,
            values=["US", "CA", "CH", "DE", "JP", "IN", "UK", "FR"],
            command=self.on_country_selected
        )
        self.country_dropdown.pack(pady=10)

        # Indicator Selection
        self.indicator_label = ctk.CTkLabel(self.left_frame, text="Choose Indicator", font=("Arial", 16))
        self.indicator_label.pack(pady=10)

        self.indicator_dropdown = ctk.CTkOptionMenu(
            self.left_frame,
            values=self.reading.get_available_indicators(),
            command=self.on_indicator_selected
        )
        self.indicator_dropdown.pack(pady=10)

        # Middle: Historical Data Display
        self.historical_data_frame = ctk.CTkFrame(self)
        self.historical_data_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.historical_data_label = ctk.CTkLabel(self.historical_data_frame, text="Historical Data", font=("Arial", 14))
        self.historical_data_label.pack(pady=10)

    def on_country_selected(self, country):
        """Handles country selection."""
        self.selected_country = country
        print(f"🌍 Country selected: {country}")

    def on_indicator_selected(self, indicator_name):
        """Handles when an indicator is selected."""
        if not self.selected_country:
            print("❌ No country selected.")
            return

        print(f"🔍 Fetching data for: '{indicator_name}' ({self.selected_country})")

        # Convert indicator names to match JSON keys
        indicator_name = indicator_name.strip().title()

        # Get the latest data from Excel
        data = self.reading.get_latest_data(indicator_name, self.selected_country)

        # Get indicator metadata from JSON mappings
        mapping_data = self.mappings.get_indicator_info(indicator_name, self.selected_country)

        if not mapping_data:
            print(f"⚠️ No metadata found for '{indicator_name}' ({self.selected_country})")
            print(f"💡 Available Indicators: {list(self.mappings.data.keys())}")
        else:
            print(f"✅ Metadata Found: {mapping_data}")

        if data:
            display_text = (
                f"Latest Data for {indicator_name} ({self.selected_country}):\n"
                f"Date: {data['date']}\n"
                f"Actual: {data['actual']}\n"
                f"Forecast: {data['forecast']}\n"
                f"Previous: {data['previous']}\n\n"
                f"Description: {mapping_data.get('description', 'No description available')}\n"
                f"Derived Via: {mapping_data.get('derived_via', 'No formula available')}\n"
                f"Acronym: {mapping_data.get('acro', 'No acronym available')}\n"
                f"Event Type: {mapping_data.get('event_type', 'No event type available')}\n"
                f"Frequency: {mapping_data.get('frequency', 'No frequency available')}\n"
                f"Source: {mapping_data.get('source', 'No source available')}\n"
                f"Usual Effect: {mapping_data.get('usual_effect', 'No effect available')}\n"
                f"Impact: {mapping_data.get('impact', 'No impact available')}"
            )
        else:
            display_text = f"No data found for {indicator_name} ({self.selected_country})."

        print(display_text)  # Debugging
        self.historical_data_label.configure(text=display_text)
