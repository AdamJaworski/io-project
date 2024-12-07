import customtkinter as ctk
import tkinter as tk
from view.audio_capture import RecordingButton
from view.new_meeting import NewMeeting
from view.generate_report import GenerateReport
from common import variables

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Geometry
        center_x = int(self.winfo_screenwidth() / 2 - int(self.winfo_screenwidth() / 1.7) / 2)
        y_offset = int(self.winfo_screenheight() / 10)
        self.y_height = int(self.winfo_screenheight() / 12)
        self.x_width = int(self.winfo_screenwidth() / 4)
        self.geometry(f'{self.x_width}x{self.y_height}+{center_x}+{y_offset}')

        self.title("")
        self.overrideredirect(False)
        #self.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.resizable(False, False)

        self.display = ctk.CTkLabel(self, height=int(self.y_height / 10), text=variables.report_id)
        self.display.pack(fill='x')
        variables.display = tk.StringVar()

        new_meeting     = NewMeeting(self)
        record_button   = RecordingButton(self)
        generate_report = GenerateReport(self)

        new_meeting.pack(side='left', fill='y')
        record_button.pack(side='left', fill='y', padx=5)
        generate_report.pack(side='left', fill='y')

        self.mainloop()

    def disable_event(self):
        pass


if __name__ ==  "__main__":
    App()
