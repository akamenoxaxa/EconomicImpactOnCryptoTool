import customtkinter as ctk
from reading import Reading
from mappings import Mappings

# Initialize classes
reading = Reading("data.xlsx")
mappings = Mappings("indicators_mapping.json")

class HistoricalDataScreen(ctk.CTkFrame):
    def __init__(self, parent, indicator, country):
        super().__init__(parent)
        self.parent = parent
        self.indicator = indicator
        self.country = country

        self.label = ctk.CTkLabel(self, text=f"Historical Data for {indicator} ({country})", font=("Arial", 18))
        self.label.pack(pady=10)

        self.data_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.data_label.pack(pady=10)

        self.display_historical_data()

    def display_historical_data(self):
        """
        Fetch and display historical data and indicator information.
        """
        data = reading.get_country_data(self.indicator, self.country)
        indicator_info = mappings.get_indicator_info(self.indicator, self.country)

        if data is not None:
            display_text = "\n".join(f"{row['date']} | {row['actual']} | {row['forecast']} | {row['previous']}" for _, row in data.iterrows())
            display_text += f"\n\nSource: {indicator_info['source']}\nImpact: {indicator_info['impact']}"
            self.data_label.configure(text=display_text)
        else:
            self.data_label.configure(text="No historical data found.")
