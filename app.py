import customtkinter as ctk
import tkinter as tk
from view.audio_capture import RecordingButton


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Geometry
        center_x = int(self.winfo_screenwidth() / 2 - int(self.winfo_screenwidth() / 1.7) / 2)
        y_offset = int(self.winfo_screenheight() / 10)
        self.y_height = int(self.winfo_screenheight() / 15)
        self.x_width = int(self.winfo_screenwidth() / 1.7)
        self.geometry(f'{self.x_width}x{self.y_height}+{center_x}+{y_offset}')

        self.title("")
        self.overrideredirect(False)
        #self.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.resizable(False, False)

        self.recording = RecordingButton(self)

        self.mainloop()


    def disable_event(self):
        pass


if __name__ ==  "__main__":
    App()
