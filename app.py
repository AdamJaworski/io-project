import customtkinter as ctk
import tkinter as tk
from view.audio_capture import RecordingButton
from view.new_meeting import NewMeeting
from view.generate_report import GenerateReport
from view.send_report import SendReport
from common import variables

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Geometry
        center_x = int(self.winfo_screenwidth() / 2 - int(self.winfo_screenwidth() / 1.7) / 2)
        y_offset = int(self.winfo_screenheight() / 10)
        self.y_height = int(self.winfo_screenheight() / 10)
        self.x_width = int(self.winfo_screenwidth() / 4)
        self.geometry(f'{self.x_width}x{self.y_height}+{center_x}+{y_offset}')

        self.title("")
        self.overrideredirect(False)
        #self.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.resizable(False, False)

        variables.report_id = tk.StringVar()
        variables.display = tk.StringVar()
        self.meeting = ctk.CTkEntry(self, height=int(self.y_height / 10), textvariable=variables.report_id, placeholder_text='Nazwa spotkania')
        self.display = ctk.CTkLabel(self, height=int(self.y_height / 10), text='Aktualny status')
        self.meeting.pack(fill='x')
        self.display.pack(fill='x', pady=3)


        new_meeting     = NewMeeting(self)
        record_button   = RecordingButton(self)
        generate_report = GenerateReport(self)
        send_report = SendReport(self)

        new_meeting.pack(side='left', fill='y')
        record_button.pack(side='left', fill='y', padx=5)
        generate_report.pack(side='left', fill='y')
        send_report.pack(side='left', fill='y', padx=(5,0))

        self.mainloop()

    def disable_event(self):
        pass


if __name__ ==  "__main__":
    App()
