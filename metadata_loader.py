import json
import os
import sys

class MetadataLoader:
    def __init__(self, file_name="indicators_mapping.json"):
        self.file_path = self.get_correct_path(file_name)
        self.metadata = self.load_metadata()

    def load_metadata(self):
        #Loads metadata from the JSON file
        with open(self.json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_correct_path(self, file_name):
        #Ensures the program finds indicators_mapping.json in the same directory as the .exe
        if getattr(sys, 'frozen', False):  #Running as an .exe
            base_path = os.path.dirname(sys.executable)  #Path of the .exe file
        else:
            base_path = os.path.abspath(".")  #Normal script execution

        return os.path.join(base_path, file_name)

    def load_metadata(self):
        #Loads the indicators mapping JSON file
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"[ERROR] Metadata file not found: {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_metadata(self, indicator, country):
        #Retrieves metadata for a given indicator and country
        indicator = indicator.strip().upper()
        country = country.upper()

        # Get metadata for the indicator
        indicator_data = self.metadata.get(indicator, {})

        # Get country-specific metadata
        country_metadata = indicator_data.get(country, {})

        # Return structured metadata or default values if missing
        return {
            "description": country_metadata.get("Description", "No description available"),
            "derived_via": country_metadata.get("Derived Via", "No formula available"),
            "acro": country_metadata.get("Acro", "No acronym available"),
            "event_type": country_metadata.get("Event type", "No event type available"),
            "frequency": country_metadata.get("Frequency", "No frequency available"),
            "source": country_metadata.get("Source", "No source available"),
            "usual_effect": country_metadata.get("Usual effect", "No usual effect available"),
            "impact": country_metadata.get("Impact", "No impact available"),
        }
