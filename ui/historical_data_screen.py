import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_reader import DataReader

class HistoricalDataScreen(ctk.CTkToplevel):
    def __init__(self, indicator, country):
        super().__init__()
        self.title(f"Historical Data for {indicator} ({country})")
        self.geometry("800x500")

        self.data_reader = DataReader("data.xlsx")
        self.indicator = indicator
        self.country = country

        self.display_chart()

    def clean_numeric(self, value):
        #Removes non-numeric characters and converts to float if possible
        try:
            if isinstance(value, str):
                value = value.replace("<", "").replace(">", "").replace("%", "").strip()
            return float(value)
        except ValueError:
            return None  #Return None for invalid data

    def display_chart(self):
        #Displays a line chart for the historical data
        data = self.data_reader.get_historical_data(self.indicator, self.country)

        if data is None or data.empty:
            label = ctk.CTkLabel(self, text="No historical data available.")
            label.pack(pady=20)
            return

        #Clean the "ACTUAL" values
        data["ACTUAL"] = data["ACTUAL"].apply(self.clean_numeric)
        data = data.dropna(subset=["ACTUAL"])  #Remove rows where conversion failed

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(data["DATE"], data["ACTUAL"], marker="o", linestyle="-", color="blue")
        ax.set_title(f"{self.indicator} Trends ({self.country})")
        ax.set_xlabel("Date")
        ax.set_ylabel("Actual Value")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
