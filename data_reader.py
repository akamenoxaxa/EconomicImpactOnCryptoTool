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
        if indicator in self.data and "COUNTRY" in self.data[indicator]:
            return sorted(self.data[indicator]["COUNTRY"].dropna().unique())
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
            "actual": self.format_numeric_value(latest_entry["ACTUAL"]),
            "forecast": self.format_numeric_value(latest_entry["FORECAST"]),
            "previous": self.format_numeric_value(latest_entry["PREVIOUS"])
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
    def format_numeric_value(value):
        """Converts values to human-readable format, handling billions (B), millions (M), and percentages."""
        try:
            if isinstance(value, str):
                value = value.replace(",", "").strip()

                if value.endswith("B"):  # Convert billions
                    return f"{float(value.replace('B', '')):.2f}B"
                elif value.endswith("M"):  # Convert millions
                    return f"{float(value.replace('M', '')):.2f}M"
                elif "%" in value or "<" in value or ">" in value:  # Handle percentage values
                    value = value.replace("<", "").replace(">", "").replace("%", "").strip()
                    return f"{float(value):.2f}%"

            return float(value)
        except ValueError:
            return "N/A"
