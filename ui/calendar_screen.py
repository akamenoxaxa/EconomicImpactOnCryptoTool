import customtkinter as ctk
from ui.historical_data_screen import HistoricalDataScreen

class CalendarScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Title Label
        self.label = ctk.CTkLabel(self, text="Calendar Screen", font=("Arial", 20))
        self.label.pack(pady=20)

        # Navigate to Historical Data
        self.historical_button = ctk.CTkButton(self, text="View Historical Data", command=self.go_to_historical)
        self.historical_button.pack(pady=10)

        # Back to MainScreen
        self.back_button = ctk.CTkButton(self, text="Back to Main Screen", command=self.go_to_main)
        self.back_button.pack(pady=10)

    def go_to_historical(self):
        # Replace CalendarScreen with HistoricalDataScreen
        self.pack_forget()
        historical_screen = HistoricalDataScreen(self.parent)
        historical_screen.pack(fill="both", expand=True)

    def go_to_main(self):
        # Replace CalendarScreen with MainScreen
        self.pack_forget()
        from ui.main_screen import MainScreen
        main_screen = MainScreen(self.parent)
        main_screen.pack(fill="both", expand=True)
