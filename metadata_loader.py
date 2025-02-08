import json

class MetadataLoader:
    def __init__(self, json_path):
        self.json_path = json_path
        self.metadata = self.load_metadata()

    def load_metadata(self):
        #Loads metadata from the JSON file
        with open(self.json_path, "r", encoding="utf-8") as file:
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
