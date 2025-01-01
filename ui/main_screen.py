import customtkinter as ctk
from calendar import monthcalendar
from datetime import datetime
import tkinter as tk

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Prevent resizing of the window
        self.parent.geometry("1280x720")  # Fixed size (16:9 aspect ratio)
        self.parent.resizable(False, False)

        # Center the window on the screen
        self.center_window()

        # Layout Configuration
        self.grid_columnconfigure(0, weight=1)  # Left: Country and Indicators
        self.grid_columnconfigure(1, weight=2)  # Middle: Historical Data
        self.grid_columnconfigure(2, weight=3)  # Right: Calendar

        # Left: Country and Indicator Selection
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Country Selection
        self.country_label = ctk.CTkLabel(self.left_frame, text="Choose Country", font=("Arial", 16))
        self.country_label.pack(pady=10)

        self.country_dropdown = ctk.CTkOptionMenu(
            self.left_frame,
            values=[
                "US", "CANADA", "CHINA", "GERMANY", "JAPAN", "INDIA", "UK", "FRANCE",
                "BRAZIL", "ITALY", "RUSSIA", "MEXICO", "AUSTRALIA", "SOUTH KOREA",
                "SPAIN", "INDONESIA", "NETHERLANDS", "TURKEY", "SAUDI ARABIA", "SWITZERLAND"
            ],
            command=self.on_country_selected
        )
        self.country_dropdown.pack(pady=10)

        # Indicator Group Selection
        self.indicator_group_label = ctk.CTkLabel(self.left_frame, text="Choose Indicator Group", font=("Arial", 16))
        self.indicator_group_label.pack(pady=10)

        self.indicator_group_dropdown = ctk.CTkOptionMenu(
            self.left_frame,
            values=["Main", "Labour", "Prices", "Trade", "GDP", "Government", "Housing", "Consumer", "Taxes"],
            command=self.on_group_selected
        )
        self.indicator_group_dropdown.pack(pady=10)

        # Indicator Buttons
        self.indicator_buttons_frame = ctk.CTkFrame(self.left_frame)
        self.indicator_buttons_frame.pack(pady=10)

        # Middle: Historical Data Display
        self.historical_data_frame = ctk.CTkFrame(self)
        self.historical_data_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.historical_data_label = ctk.CTkLabel(self.historical_data_frame, text="", font=("Arial", 14))
        self.historical_data_label.pack(pady=10)

        # Right: Calendar
        self.calendar_frame = ctk.CTkFrame(self, corner_radius=10)
        self.calendar_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.calendar_label = ctk.CTkLabel(self.calendar_frame, text="", font=("Arial", 16))
        self.calendar_label.pack(pady=10)

        self.calendar_days = ctk.CTkLabel(self.calendar_frame, text="", justify="left", font=("Courier", 16))  # Bigger font
        self.calendar_days.pack(pady=20)

        self.show_calendar()

    def center_window(self):
        """Center the window on the screen."""
        self.parent.update_idletasks()
        width = 1280
        height = 720
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.parent.geometry(f"{width}x{height}+{x}+{y}")

    def on_country_selected(self, country):
        print(f"Selected Country: {country}")

    def on_group_selected(self, group):
        print(f"Selected Group: {group}")
        self.show_indicators(group)

    def show_indicators(self, group):
        # Clear any existing buttons
        for widget in self.indicator_buttons_frame.winfo_children():
            widget.destroy()

        # Indicators by Group
        indicators_by_group = {
            "Main": ["GDP", "CPI"],
            "Labour": ["Unemployment", "Wages"],
            "Prices": ["Inflation"],
            "GDP": ["GDP", "GDP Full Year Growth"],
            # Add other groups as needed
        }

        indicators = indicators_by_group.get(group, [])
        for indicator in indicators:
            button = ctk.CTkButton(
                self.indicator_buttons_frame,
                text=indicator,
                command=lambda ind=indicator: self.on_indicator_selected(ind),
                width=200  # Fixed button width to avoid resizing
            )
            button.pack(pady=5)

    def on_indicator_selected(self, indicator):
        print(f"Selected Indicator: {indicator}")
        self.show_historical_data(indicator)

    def show_historical_data(self, indicator):
        # Clear existing historical data
        for widget in self.historical_data_frame.winfo_children():
            widget.destroy()

        # Add a title
        title = ctk.CTkLabel(self.historical_data_frame, text=f"Historical Data for {indicator}", font=("Arial", 16))
        title.pack(pady=10)

        # Sample Historical Data Blocks
        samples = [
            {"date": "2023-01-01", "impact": "Positive"},
            {"date": "2022-12-01", "impact": "Neutral"},
            {"date": "2022-11-01", "impact": "Negative"},
            {"date": "2022-10-01", "impact": "Positive"},
        ]

        for sample in samples:
            block = ctk.CTkFrame(self.historical_data_frame, corner_radius=10)
            block.pack(fill="x", pady=5, padx=10)
            label = ctk.CTkLabel(
                block,
                text=f"Date: {sample['date']} | Impact: {sample['impact']}",
                anchor="w",  # Align text to the left
                font=("Arial", 12)
            )
            label.pack(fill="x", padx=10, pady=5)

    def show_calendar(self):
        # Get the current month and year
        now = datetime.now()
        year, month = now.year, now.month
        day_today = now.day
        month_name = now.strftime("%B")

        # Set calendar label with current month name
        self.calendar_label.configure(text=f"Current Month - {month_name}")

        # Generate calendar days
        month_days = monthcalendar(year, month)

        # Display calendar days
        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        calendar_str = " ".join(week_days) + "\n\n"

        for week in month_days:
            week_str = ""
            for day in week:
                if day == day_today:
                    week_str += f"[{day:>2}]"  # Highlight current day
                else:
                    week_str += f"{day:>3} " if day != 0 else "    "
            calendar_str += week_str + "\n"

        self.calendar_days.configure(text=calendar_str)
