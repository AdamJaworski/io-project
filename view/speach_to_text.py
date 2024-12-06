import customtkinter as ctk
from controller.speach_to_text import start_recording, stop_recording, get_entire_recording_transcript
from uuid import uuid1


class RecordingButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent, width=int(parent.x_width / 10), command=self.button_press, text='Start Recording')

        self.parent = parent
        self.recoding = False
        self.hover = False

        self.current_report_id = None

        self.current_timer = -0.1
        self.pack(side='left', fill='y')


        self.bind('<Enter>', self.__change_hover)
        self.bind('<Leave>', self.__change_hover)


    def __change_hover(self, *args):
        self.hover = not self.hover

    def button_press(self):
        self.recoding = not self.recoding

        if self.recoding:
            self.current_report_id = str(uuid1())
            start_recording(self.current_report_id)
            self.recoding = True
            self.update_timer()

        else:
            stop_recording()
            transcript = get_entire_recording_transcript(self.current_report_id)
            print(transcript)
            self.configure(text='Start recording')
            self.current_timer = -0.1

    def update_timer(self):
        if self.recoding:
            self.current_timer += 0.1
            configure_text = f'{self.current_timer:.1f}s' if not self.hover else 'Stop recording'
            self.configure(text=configure_text)
            self.after(100, self.update_timer)
