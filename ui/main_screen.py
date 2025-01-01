import customtkinter as ctk
from ui.calendar_screen import CalendarScreen

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Title Label
        self.label = ctk.CTkLabel(self, text="Select Economic Indicators", font=("Arial", 20))
        self.label.pack(pady=20)

        # Indicator Selection
        self.indicator_list = ctk.CTkOptionMenu(self, values=["GDP", "CPI", "Unemployment", "Interest Rate"])
        self.indicator_list.pack(pady=10)

        # Next Button
        self.next_button = ctk.CTkButton(self, text="Go to Calendar", command=self.go_to_calendar)
        self.next_button.pack(pady=10)

    def go_to_calendar(self):
        # Replace MainScreen with CalendarScreen
        self.pack_forget()
        calendar_screen = CalendarScreen(self.parent)
        calendar_screen.pack(fill="both", expand=True)
