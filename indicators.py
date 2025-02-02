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
