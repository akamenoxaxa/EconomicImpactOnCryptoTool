import customtkinter as ctk
import pandas as pd


class DateSelector(ctk.CTkToplevel):
    def __init__(self, indicator, country, data_reader):
        super().__init__()

        self.indicator = indicator
        self.country = country
        self.data_reader = data_reader

        self.title(f"Select Date - {self.indicator} ({self.country})")
        self.geometry("400x300")

        # **Dropdowns for Year & Month Selection**
        self.year_var = ctk.StringVar(value="Select Year")
        self.month_var = ctk.StringVar(value="Select Month")

        self.year_dropdown = ctk.CTkOptionMenu(self, variable=self.year_var, values=self.get_available_years())
        self.year_dropdown.pack(pady=10)

        self.month_dropdown = ctk.CTkOptionMenu(self, variable=self.month_var, values=self.get_available_months())
        self.month_dropdown.pack(pady=10)

        # **Submit Button**
        self.submit_button = ctk.CTkButton(self, text="Check Data", command=self.fetch_data)
        self.submit_button.pack(pady=10)

        # **Result Label**
        self.result_label = ctk.CTkLabel(self, text="Data will appear here", font=("Arial", 14))
        self.result_label.pack(pady=20)

    def get_available_years(self):
        #Fetches available years from the dataset
        data = self.data_reader.get_historical_data(self.indicator, self.country)
        if data is None or data.empty:
            return []

        data["DATE"] = pd.to_datetime(data["DATE"], errors="coerce")
        return sorted(data["DATE"].dt.year.dropna().astype(str).unique(), reverse=True)

    def get_available_months(self):
        #Returns months in 'MM' format
        return [str(i).zfill(2) for i in range(1, 13)]  # ['01', '02', ..., '12']

    def fetch_data(self):
        #Fetches data for the selected year and month
        selected_year = self.year_var.get()
        selected_month = self.month_var.get()

        if selected_year == "Select Year" or selected_month == "Select Month":
            self.result_label.configure(text="Please select a valid year and month", text_color="red")
            return

        #Fetch historical data
        data = self.data_reader.get_historical_data(self.indicator, self.country)
        if data is None or data.empty:
            self.result_label.configure(text="No data available", text_color="red")
            return

        data["DATE"] = pd.to_datetime(data["DATE"], errors="coerce")
        selected_date = f"{selected_year}-{selected_month}"

        #Filter for selected date
        filtered_data = data[data["DATE"].dt.strftime("%Y-%m") == selected_date]

        if not filtered_data.empty:
            actual_value = filtered_data["ACTUAL"].values[0]
            self.result_label.configure(text=f"Actual: {actual_value}", text_color="green")
        else:
            self.result_label.configure(text="N/A", text_color="red")
