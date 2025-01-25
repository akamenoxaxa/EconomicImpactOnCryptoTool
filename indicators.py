class Indicator:
    def __init__(self, name, description, derived_via, acro, event_type):
        self.name = name
        self.description = description
        self.derived_via = derived_via
        self.acro = acro
        self.event_type = event_type

    def display_info(self):
        return (
            f"Indicator: {self.name}\n"
            f"Description: {self.description}\n"
            f"Derived Via: {self.derived_via}\n"
            f"Abbreviation: {self.acro}\n"
            f"Event Type: {self.event_type}\n"
        )


class CPI(Indicator):
    def __init__(self, country, general_data, country_data):
        super().__init__(
            name="CPI",
            description=general_data["Description"],
            derived_via=general_data["Derived Via"],
            acro=general_data["Acro"],
            event_type=general_data["Event type"],
        )
        self.country = country
        self.frequency = country_data.get("Frequency", "Unknown Frequency/Error")
        self.source = country_data.get("Source", "Unknown Source/Error")
        self.usual_effect = country_data.get("Usual effect", "Unknown Effect/Error")
        self.impact = country_data.get("Impact", "Unknown Impact/Error")

    def display_info(self):
        base_info = super().display_info()
        return (
            f"{base_info}\n"
            f"Country: {self.country}\n"
            f"Frequency: {self.frequency}\n"
            f"Source: {self.source}\n"
            f"Usual Effect: {self.usual_effect}\n"
            f"Impact: {self.impact}\n"
        )


class GDP(Indicator):
    def __init__(self, country, general_data, country_data):
        super().__init__(
            name="GDP",
            description=general_data["Description"],
            derived_via=general_data["Derived Via"],
            acro=general_data["Acro"],
            event_type=general_data["Event type"],
        )
        self.country = country
        self.frequency = country_data.get("Frequency", "Unknown Frequency/Error")
        self.source = country_data.get("Source", "Unknown Source/Error")
        self.usual_effect = country_data.get("Usual effect", "Unknown Effect/Error")
        self.impact = country_data.get("Impact", "Unknown Impact/Error")

    def display_info(self):
        base_info = super().display_info()
        return (
            f"{base_info}\n"
            f"Country: {self.country}\n"
            f"Frequency: {self.frequency}\n"
            f"Source: {self.source}\n"
            f"Usual Effect: {self.usual_effect}\n"
            f"Impact: {self.impact}\n"
        )




OR THIS CODE

"""
class Indicator:
    def __init__(self, name, description, derived_via, acro, event_type):
        """
        Base class for indicators.

        Args:
        - name: The name of the indicator.
        - description: The description of the indicator.
        - derived_via: How the indicator is calculated.
        - acro: The indicator's abbreviation or acronym.
        - event_type: The type of event the indicator represents.
        """
        self.name = name
        self.description = description
        self.derived_via = derived_via
        self.acro = acro
        self.event_type = event_type

    def display_info(self):
        """
        Display general information about the indicator.
        """
        return (
            f"Indicator: {self.name}\n"
            f"Description: {self.description}\n"
            f"Derived Via: {self.derived_via}\n"
            f"Abbreviation: {self.acro}\n"
            f"Event Type: {self.event_type}\n"
        )


class CountrySpecificIndicator(Indicator):
    def __init__(self, name, general_data, country, country_data):
        """
        Country-specific indicator class, extending Indicator.

        Args:
        - name: Name of the indicator (e.g., "CPI").
        - general_data: General information about the indicator (from JSON).
        - country: Country code (e.g., "US").
        - country_data: Country-specific details (from JSON).
        """
        super().__init__(
            name=name,
            description=general_data.get("Description", "Unknown description"),
            derived_via=general_data.get("Derived Via", "Unknown derived via"),
            acro=general_data.get("Acro", "Unknown acronym"),
            event_type=general_data.get("Event type", "Unknown event type"),
        )
        self.country = country
        self.frequency = country_data.get("Frequency", "Unknown frequency")
        self.source = country_data.get("Source", "Unknown source")
        self.usual_effect = country_data.get("Usual effect", "Unknown usual effect")
        self.impact = country_data.get("Impact", "Unknown impact")

    def display_info(self):
        """
        Display full information, including country-specific details.
        """
        base_info = super().display_info()
        return (
            f"{base_info}\n"
            f"Country: {self.country}\n"
            f"Frequency: {self.frequency}\n"
            f"Source: {self.source}\n"
            f"Usual Effect: {self.usual_effect}\n"
            f"Impact: {self.impact}\n"
        )

"""