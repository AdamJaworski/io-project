import uuid
import customtkinter as ctk
from controller.audio_capture import start_recording, stop_recording
from common import variables

class NewMeeting(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent, width=int(parent.x_width / 4), text='New Meeting', command=self.generate_new_meeting_id)

        self.parent = parent
        self.pack(side='left', fill='y')


    def generate_new_meeting_id(self):
        variables.report_id = str(uuid.uuid1())
        self.parent.meeting.set(variables.report_id)