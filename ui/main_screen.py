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
        """Configures UI layout with fixed text area size."""
        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.indicator_menu = ctk.CTkOptionMenu(self, values=["Loading..."], command=self.on_indicator_selected)
        self.indicator_menu.grid(row=0, column=0, padx=20, pady=10)

        self.country_menu = ctk.CTkOptionMenu(self, values=["Select Indicator First"], command=self.on_country_selected)
        self.country_menu.grid(row=1, column=0, padx=20, pady=10)

        self.data_label = ctk.CTkTextbox(self, wrap="word", width=600, height=250)
        self.data_label.grid(row=0, column=1, rowspan=3, padx=20, pady=10, sticky="w")

        self.chart_button = ctk.CTkButton(self, text="View Historical Chart", command=self.open_chart, state="disabled")
        self.chart_button.grid(row=3, column=0, padx=20, pady=10)

    def populate_indicators(self):
        """Populates indicator dropdown dynamically."""
        indicators = self.data_reader.get_available_indicators()
        self.indicator_menu.configure(values=indicators)

    def on_indicator_selected(self, indicator):
        """Handles indicator selection."""
        self.selected_indicator = indicator.strip().upper()
        countries = self.data_reader.get_available_countries(indicator)
        self.country_menu.configure(values=countries)
        self.country_menu.set("Country")

    def on_country_selected(self, country):
        """Handles country selection and displays data."""
        self.selected_country = country.upper()
        data = self.data_reader.get_latest_data(self.selected_indicator, self.selected_country)
        metadata = self.metadata_loader.get_metadata(self.selected_indicator, self.selected_country)

        if data:
            display_text = f"Latest {self.selected_indicator} ({self.selected_country}):\n" \
                           f"Date: {data['date']}\n" \
                           f"Actual: {data['actual']}\n" \
                           f"Forecast: {data['forecast']}\n" \
                           f"Previous: {data['previous']}\n\n" \
                           f"📌 **Metadata:**\n" \
                           f"🔹 Description: {metadata['description']}\n" \
                           f"🔹 Derived Via: {metadata['derived_via']}\n" \
                           f"🔹 Acronym: {metadata['acro']}\n" \
                           f"🔹 Event Type: {metadata['event_type']}\n" \
                           f"🔹 Frequency: {metadata['frequency']}\n" \
                           f"🔹 Source: {metadata['source']}\n" \
                           f"🔹 Usual Effect: {metadata['usual_effect']}\n" \
                           f"🔹 Impact: {metadata['impact']}"
        else:
            display_text = "No data available."

        self.data_label.delete("1.0", "end")
        self.data_label.insert("1.0", display_text)
        self.chart_button.configure(state="normal")

    def open_chart(self):
        """Opens a new window to display historical data."""
        if self.selected_indicator and self.selected_country:
            HistoricalDataScreen(self.selected_indicator, self.selected_country)
