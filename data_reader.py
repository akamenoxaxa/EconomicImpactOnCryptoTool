import pandas as pd

class DataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """Loads all sheets from the Excel file dynamically with normalized names."""
        sheets = pd.read_excel(self.file_path, sheet_name=None)
        return {name.strip().upper(): df for name, df in sheets.items()}

    def get_available_indicators(self):
        """Returns all sheet names as available indicators."""
        return list(self.data.keys())

    def get_available_countries(self, indicator):
        """Returns a list of unique countries available for the selected indicator."""
        indicator = indicator.strip().upper()
        if indicator in self.data:
            return sorted(self.data[indicator]["COUNTRY"].unique())
        return []

    def get_latest_data(self, indicator, country):
        """Fetches the latest available data for a given indicator and country."""
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
            "actual": self.convert_numeric(latest_entry["ACTUAL"]),
            "forecast": self.convert_numeric(latest_entry["FORECAST"]),
            "previous": self.convert_numeric(latest_entry["PREVIOUS"])
        }

    def get_historical_data(self, indicator, country):
        """Fetches all historical data for a given indicator and country."""
        indicator = indicator.strip().upper()
        if indicator not in self.data:
            return None

        df = self.data[indicator]
        df = df[df["COUNTRY"] == country].copy()

        if df.empty:
            return None

        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df.sort_values(by="DATE", ascending=True)

        return df[["DATE", "ACTUAL"]]

    @staticmethod
    def convert_numeric(value):
        """Converts values like '<0.10%' to numeric, handling special cases."""
        try:
            if isinstance(value, str):
                if "<" in value or ">" in value:
                    value = value.replace("<", "").replace(">", "").replace("%", "").strip()
                return float(value)
            return float(value)
        except ValueError:
            return None
