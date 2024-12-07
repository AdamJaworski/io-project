import customtkinter as ctk
import tkinter as tk
from view.audio_capture import RecordingButton
from view.new_meeting import NewMeeting
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

        self.label = ctk.CTkLabel(self, height=int(self.y_height/10), text=variables.report_id)
        self.label.pack(fill='x')
        self.meeting = tk.StringVar(self.label)
        self.meeting.trace_add('write', self.update_meeting)

        NewMeeting(self)
        self.recording = RecordingButton(self)

        self.mainloop()

    def update_meeting(self, *args):
        self.label.configure(text=self.meeting.get())
    def disable_event(self):
        pass


if __name__ ==  "__main__":
    App()
