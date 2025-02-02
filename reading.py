import pandas as pd
import os

# Country mapping dictionary
COUNTRY_MAPPING = {
    "United States": "US", "China": "CH", "Australia": "AU", "Canada": "CA",
    "United Kingdom": "UK", "Switzerland": "SZ", "Germany": "DE", "France": "FR",
    "Japan": "JP", "India": "IN", "Mexico": "MX", "South Korea": "KR",
    "Brazil": "BR", "Netherlands": "NL", "Spain": "ES", "Indonesia": "ID",
    "Turkey": "TR", "Saudi Arabia": "SA", "Italy": "IT", "Russia": "RU"
}

class Reading:
    def __init__(self, file_path):
        """
        Initializes the Reading class and loads all sheets into memory.
        Args:
        - file_path: Path to the Excel file.
        """
        self.file_path = os.path.join(os.path.dirname(__file__), file_path)

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Data file '{self.file_path}' not found.")

        # Load all sheets into memory
        self.data = pd.read_excel(self.file_path, sheet_name=None)

        # Standardize column names and clean data
        for sheet in self.data:
            df = self.data[sheet]

            # Ensure all column names are lowercase and stripped of spaces
            df.columns = df.columns.str.strip().str.lower()

            # Rename 'country' column to ensure compatibility
            if "country" in df.columns:
                df.rename(columns={"country": "country"}, inplace=True)

            # Strip spaces from country names
            df["country"] = df["country"].str.strip()

            # Convert date column to proper datetime format
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"].astype(str).str.strip(), errors="coerce")

            # Convert numeric columns to floats
            for col in ["actual", "forecast", "previous"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

            # Save cleaned dataframe
            self.data[sheet] = df

    def get_available_indicators(self):
        """ Returns a list of all available economic indicators (sheet names). """
        return list(self.data.keys())

    def get_data_for_indicator(self, indicator):
        """ Returns the DataFrame for a specific economic indicator. """
        if indicator in self.data:
            df = self.data[indicator]
            print(f"✅ Found Indicator: {indicator}")  # Debugging
            print(f"Columns: {df.columns.tolist()}")
            return df
        else:
            print(f"❌ Indicator '{indicator}' not found in data.xlsx.")
            return None

    def get_country_data(self, indicator, country):
        """ Returns all data for a specific country from a given indicator. """
        df = self.get_data_for_indicator(indicator)
        if df is not None:
            country = COUNTRY_MAPPING.get(country, country).strip().upper()  # Convert full name to acronym

            available_countries = df["country"].unique()
            print(f"Available countries in {indicator}: {available_countries}")  # Debugging

            if country in available_countries:
                return df[df["country"] == country]
            else:
                print(f"❌ No data found for country '{country}' in {indicator}.")
        return None

    def get_latest_data(self, indicator, country):
        """ Returns the latest available data for a specific indicator and country. """
        df = self.get_country_data(indicator, country)
        if df is not None and not df.empty:
            df = df.sort_values(by="date", ascending=False)
            latest_data = df.iloc[0] if not df.empty else None
            return latest_data.to_dict() if latest_data is not None else None
        return None
