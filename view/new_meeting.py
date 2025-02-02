import uuid
import customtkinter as ctk
from common import variables
from common.button import Button

class NewMeeting(Button):
    def __init__(self, parent):
        super().__init__(parent, width=int(parent.x_width / 4) - 5, text='Nowe Spotkanie', command=self.set_new_meeting_id)
        self.parent = parent


    def set_new_meeting_id(self):
        variables.report_id.set(str(uuid.uuid1()))
        #self.parent.display.configure(text=variables.report_id)