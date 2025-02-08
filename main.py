import customtkinter as ctk
from ui.main_screen import MainScreen

class CryptoAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Analysis Tool")
        self.geometry("1280x720")  # 16:9 Aspect Ratio
        self.resizable(False, False)
        self.main_screen = MainScreen(self)
        self.main_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = CryptoAnalysisApp()
    app.mainloop()
