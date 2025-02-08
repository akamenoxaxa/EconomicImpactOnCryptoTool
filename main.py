import customtkinter as ctk
from ui.main_screen import MainScreen
import sys

class CryptoAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Analysis Tool")
        self.geometry("1280x720")  # 16:9 Aspect Ratio
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)  #Handle window close event
        self.main_screen = MainScreen(self)
        self.main_screen.pack(fill="both", expand=True)

    def on_close(self):
        #Ensures the application fully exits when closed
        print("[INFO] Closing application...")
        self.destroy()  #Closes Tkinter properly
        sys.exit(0)  #Ensures all processes are terminated

if __name__ == "__main__":
    app = CryptoAnalysisApp()
    app.mainloop()
