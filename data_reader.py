import pandas as pd
import os
import sys


class DataReader:
    def __init__(self, file_name="data.xlsx"):
        self.file_path = self.get_correct_path(file_name)
        self.data = self.load_data()

    def load_data(self):
        #Loads all sheets from the Excel file dynamically with normalized names
        sheets = pd.read_excel(self.file_path, sheet_name=None)
        return {name.strip().upper(): df for name, df in sheets.items()}

    def get_available_indicators(self):
        #Returns all sheet names as available indicators
        return list(self.data.keys())

    def get_available_countries(self, indicator):
        #Returns a list of unique countries available for the selected indicator
        indicator = indicator.strip().upper()
        if indicator in self.data and "COUNTRY" in self.data[indicator]:
            return sorted(self.data[indicator]["COUNTRY"].dropna().unique())
        return []

    def get_latest_data(self, indicator, country):
        #Fetches the latest available data for a given indicator and country
        indicator = indicator.strip().upper()
        if indicator not in self.data:
            return None

        df = self.data[indicator]
        df = df[df["COUNTRY"] == country].copy()

        if df.empty:
            return None

        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df.sort_values(by="DATE", ascending=False)
        latest_entry = df.iloc[0]

        return {
            "date": latest_entry["DATE"].strftime("%Y-%m-%d"),
            "actual": self.append_parameter(latest_entry["ACTUAL"], latest_entry["PARAMETER"]),
            "forecast": self.append_parameter(latest_entry["FORECAST"], latest_entry["PARAMETER"]),
            "previous": self.append_parameter(latest_entry["PREVIOUS"], latest_entry["PARAMETER"])
        }

    def get_historical_data(self, indicator, country):
        #Fetches all historical data for a given indicator and country
        indicator = indicator.strip().upper()
        if indicator not in self.data:
            return None

        df = self.data[indicator]
        df = df[df["COUNTRY"] == country].copy()

        if df.empty:
            return None

        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df.sort_values(by="DATE", ascending=True)

        df["ACTUAL"] = df.apply(lambda row: self.append_parameter(row["ACTUAL"], row["PARAMETER"]), axis=1)

        return df[["DATE", "ACTUAL"]]

    def get_correct_path(self, file_name):
        #Ensures the program finds data.xlsx in the same directory as the .exe
        if getattr(sys, 'frozen', False):  #Running as an .exe
            base_path = os.path.dirname(sys.executable)  #Path of the .exe file
        else:
            base_path = os.path.abspath(".")  #Normal script execution

        return os.path.join(base_path, file_name)

    def load_data(self):
        #Loads all sheets from the Excel file dynamically with normalized names
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"[ERROR] Data file not found: {self.file_path}")

        sheets = pd.read_excel(self.file_path, sheet_name=None)
        return {name.strip().upper(): df for name, df in sheets.items()}

    @staticmethod
    def append_parameter(value, parameter):
        #Appends the corresponding parameter (e.g., %, B) to the value without modifying the numeric value
        if pd.isna(value) or pd.isna(parameter):
            return str(value)  # Keeps NaN values as is

        return f"{value}{parameter.strip()}" if isinstance(parameter, str) else str(value)
