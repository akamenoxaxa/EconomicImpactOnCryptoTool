import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HistoricalDataScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title Label
        self.label = ctk.CTkLabel(self, text="Historical Data", font=("Arial", 20))
        self.label.pack(pady=20)

        # Matplotlib Chart
        self.plot_chart()

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back to Calendar", command=self.go_to_calendar)
        self.back_button.pack(pady=10)

    def plot_chart(self):
        # Create a sample Matplotlib figure
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot([1, 2, 3], [10, 20, 15], label="Sample Data")
        ax.set_title("Economic Indicator Impact")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()

        # Embed Matplotlib figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def go_to_calendar(self):
        # Replace HistoricalDataScreen with CalendarScreen
        self.pack_forget()
        from ui.calendar_screen import CalendarScreen
        calendar_screen = CalendarScreen(self.parent)
        calendar_screen.pack(fill="both", expand=True)
