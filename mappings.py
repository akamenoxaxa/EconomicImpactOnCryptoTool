import json
import os
from reading import COUNTRY_MAPPING  # Import country mapping from reading.py

class Mappings:
    def __init__(self, file_path):
        """
        Initializes the Mappings class and loads the indicator mappings JSON file.
        Args:
        - file_path: Path to the JSON file.
        """
        self.file_path = os.path.join(os.path.dirname(__file__), file_path)

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Mappings file '{self.file_path}' not found.")

        with open(self.file_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def get_indicator_info(self, indicator, country):
        """
        Returns all relevant details for a given indicator and country.
        Args:
        - indicator: Economic indicator name.
        - country: Country name (full or acronym).
        """
        # Convert indicator name to title case for exact matching
        indicator = indicator.strip().title()

        # Convert country name to acronym if needed
        country_acronym = COUNTRY_MAPPING.get(country, country).upper()

        # DEBUG: Print available indicators and countries
        print(f"🔍 Looking up '{indicator}' ({country_acronym}) in JSON...")
        available_indicators = list(self.data.keys())
        print(f"✅ Available Indicators in JSON: {available_indicators}")

        if indicator not in self.data:
            print(f"❌ Indicator '{indicator}' NOT found in mappings.")
            return None

        indicator_data = self.data[indicator]

        # Root-level metadata (general information for the indicator)
        global_metadata = {
            "description": indicator_data.get("Description"),
            "derived_via": indicator_data.get("Derived Via"),
            "acro": indicator_data.get("Acro"),
            "event_type": indicator_data.get("Event type"),
        }

        # Check if country exists
        available_countries = indicator_data.get("Countries", {}).keys()
        print(f"🌍 Available Countries for {indicator}: {available_countries}")

        if country_acronym not in available_countries:
            print(f"❌ Country '{country_acronym}' NOT found for indicator '{indicator}'.")
            return None

        country_data = indicator_data["Countries"][country_acronym]

        # Use root-level metadata if available, otherwise use country-level metadata
        merged_data = {
            "description": global_metadata["description"] or country_data.get("Description", "No description available"),
            "derived_via": global_metadata["derived_via"] or country_data.get("Derived Via", "No formula available"),
            "acro": global_metadata["acro"] or country_data.get("Acro", "No acronym available"),
            "event_type": global_metadata["event_type"] or country_data.get("Event type", "No event type available"),
            "frequency": country_data.get("Frequency", "No frequency available"),
            "source": country_data.get("Source", "No source available"),
            "usual_effect": country_data.get("Usual effect", "No effect available"),
            "impact": country_data.get("Impact", "No impact available"),
        }

        return merged_data
