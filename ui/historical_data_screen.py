import customtkinter as ctk


class HistoricalDataScreen(ctk.CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.parent = parent

        # Configure the new window
        self.parent.geometry("800x600")  # Fixed size for the new window
        self.parent.title("Historical Data Details")
        self.pack(fill="both", expand=True)

        # Add a title
        self.title_label = ctk.CTkLabel(
            self, text="Historical Data Details", font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=20)

        # Display the selected data
        self.data_label = ctk.CTkLabel(
            self,
            text=f"Date: {data['date']}\nImpact: {data['impact']}",
            font=("Arial", 14),
            anchor="center",
            justify="center",
        )
        self.data_label.pack(pady=10)

        # Add a "Close" button
        self.close_button = ctk.CTkButton(
            self, text="Close", command=self.parent.destroy, width=200
        )
        self.close_button.pack(pady=20)
