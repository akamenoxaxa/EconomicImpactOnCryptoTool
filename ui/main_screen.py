import customtkinter as ctk
from data_reader import DataReader
from metadata_loader import MetadataLoader
from ui.historical_data_screen import HistoricalDataScreen
import webbrowser


class MainScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.data_reader = DataReader("data.xlsx")
        self.metadata_loader = MetadataLoader("indicators_mapping.json")

        self.selected_indicator = None
        self.selected_country = None
        self.source_url = ""

        self.configure_layout()
        self.populate_indicators()

    def configure_layout(self):
        """Configures the UI layout properly without conflicts."""
        self.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Indicator Dropdown
        self.indicator_menu = ctk.CTkOptionMenu(self, values=["Loading..."], command=self.on_indicator_selected)
        self.indicator_menu.grid(row=1, column=0, padx=20, pady=10)

        # Country Dropdown
        self.country_menu = ctk.CTkOptionMenu(self, values=["Select Indicator First"], command=self.on_country_selected)
        self.country_menu.grid(row=2, column=0, padx=20, pady=10)

        # Main Display Box (Initially Hidden)
        self.main_display_box = ctk.CTkFrame(self, width=700, height=300, corner_radius=8)
        self.main_display_box.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.main_display_box.grid_remove()  # Hide initially

        # Title (Centered)
        self.title_label = ctk.CTkLabel(self.main_display_box, text="", font=("Arial", 22, "bold"), anchor="center")
        self.title_label.pack(pady=5)

        # Mini Data Box (Inside Main Display)
        self.data_box = ctk.CTkFrame(self.main_display_box, width=250, height=150, corner_radius=8)
        self.data_box.pack(pady=5, padx=10, anchor="w")
        self.data_box.pack_forget()  # Initially hidden

        self.date_label = ctk.CTkLabel(self.data_box, text="Date: ", font=("Arial", 14, "bold"))
        self.date_label.pack(pady=2)

        self.actual_label = ctk.CTkLabel(self.data_box, text="Actual: ", font=("Arial", 14))
        self.actual_label.pack()

        self.forecast_label = ctk.CTkLabel(self.data_box, text="Forecast: ", font=("Arial", 14))
        self.forecast_label.pack()

        self.previous_label = ctk.CTkLabel(self.data_box, text="Previous: ", font=("Arial", 14))
        self.previous_label.pack()

        # Metadata Box
        self.data_label = ctk.CTkTextbox(self.main_display_box, wrap="word", width=600, height=150)
        self.data_label.pack(pady=10)

        # Source Button (Initially Hidden)
        self.source_button = ctk.CTkButton(self.main_display_box, text="Source", command=self.open_source, fg_color="transparent", text_color="blue")
        self.source_button.pack(pady=5)
        self.source_button.pack_forget()  # Initially hidden

        # **Chart Button (Now Works Perfectly!)**
        self.chart_button = ctk.CTkButton(self, text="View Historical Chart", command=self.open_chart, state="disabled")
        self.chart_button.grid(row=3, column=0, padx=20, pady=10)
        self.chart_button.grid_remove()  # Initially hidden

    def populate_indicators(self):
        """Loads indicators dynamically from the Excel file."""
        indicators = self.data_reader.get_available_indicators()
        self.indicator_menu.configure(values=indicators)

    def on_indicator_selected(self, indicator):
        """Handles indicator selection and loads available countries."""
        self.selected_indicator = indicator.strip().upper()
        countries = self.data_reader.get_available_countries(indicator)
        self.country_menu.configure(values=countries)
        self.country_menu.set("Country")
        self.main_display_box.grid_remove()  # Hide everything until country is selected

    def on_country_selected(self, country):
        """Handles country selection and updates UI with data."""
        self.selected_country = country.upper()
        data = self.data_reader.get_latest_data(self.selected_indicator, self.selected_country)
        metadata = self.metadata_loader.get_metadata(self.selected_indicator, self.selected_country)

        if not data or not metadata:
            self.main_display_box.grid_remove()  # Hide UI if no data
            self.chart_button.grid_remove()  # Hide chart button
            return

        # Show Main Display Box
        self.main_display_box.grid()

        # Show Mini Data Box
        self.data_box.pack()

        # Update Title
        self.title_label.configure(text=self.selected_indicator)

        # Update Mini Data Box
        self.date_label.configure(text=f"Date: {data['date']}")
        self.update_value_color(self.actual_label, "Actual", data["actual"], data["previous"])
        self.forecast_label.configure(text=f"Forecast: {data['forecast']}")
        self.previous_label.configure(text=f"Previous: {data['previous']}")

        # Update Metadata Box
        impact_text, impact_color = self.get_impact_color(metadata["impact"])

        display_text = f"🔹 Description: {metadata['description']}\n" \
                       f"🔹 Derived Via: {metadata['derived_via']}\n" \
                       f"🔹 Acronym: {metadata['acro']}\n" \
                       f"🔹 Event Type: {metadata['event_type']}\n" \
                       f"🔹 Frequency: {metadata['frequency']}\n" \
                       f"🔹 Usual Effect: {metadata['usual_effect']}\n" \
                       f"🔹 Impact: {impact_text}"

        self.data_label.delete("1.0", "end")
        self.data_label.insert("1.0", display_text)
        self.data_label.configure(text_color="white")  # Set standard color

        # Show Source Button
        self.source_url = metadata["source"]
        self.source_button.configure(text="Source", command=self.open_source)
        self.source_button.pack()

        # **Enable & Show Chart Button**
        self.chart_button.configure(state="normal")
        self.chart_button.grid()

    def update_value_color(self, label, prefix, actual, previous):
        """Updates the color of the Actual value based on comparison."""
        try:
            actual = float(actual)
            previous = float(previous)
            color = "red" if actual > previous else "green"
            label.configure(text=f"{prefix}: {actual}", text_color=color)
        except ValueError:
            label.configure(text=f"{prefix}: {actual}", text_color="white")

    def get_impact_color(self, impact_text):
        """Determines the color of the Impact text based on severity."""
        impact_text = impact_text.upper()
        if "LOW" in impact_text and "MEDIUM" not in impact_text:
            return impact_text, "green"
        elif "MEDIUM" in impact_text or "LOW/MEDIUM" in impact_text:
            return impact_text, "yellow"
        elif "HIGH" in impact_text or "MEDIUM/HIGH" in impact_text:
            return impact_text, "red"
        return impact_text, "white"

    def open_source(self):
        """Opens the source URL in a web browser."""
        if self.source_url:
            webbrowser.open(self.source_url)

    def open_chart(self):
        """Opens a new window to display historical data. **NOW FIXED!**"""
        if self.selected_indicator and self.selected_country:
            HistoricalDataScreen(self.selected_indicator, self.selected_country)
