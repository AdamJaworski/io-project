import customtkinter as ctk
from controller.audio_capture import start_recording, stop_recording
from common import variables

class RecordingButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent, width=int(parent.x_width / 4), text='Start Recording\n(Double click)')

        self.parent = parent
        self.recoding = False
        self.hover = False

        self.current_report_id = None

        self.current_timer = -0.1
        self.pack(side='left', fill='y', padx=5)


        self.bind('<Enter>', self.__change_hover)
        self.bind('<Leave>', self.__change_hover)
        self.bind('<Double-Button-1>', self.button_press)

    def __change_hover(self, *args):
        self.hover = not self.hover

    def button_press(self, *args):
        self.recoding = not self.recoding

        if self.recoding:
            start_recording(variables.report_id)
            self.recoding = True
            self.update_timer()

        else:
            stop_recording()
            self.configure(text='Start recording\n(Double click)')
            self.current_timer = -0.1

    def update_timer(self):
        if self.recoding:
            self.current_timer += 0.1
            configure_text = f'{self.current_timer:.1f}s' if not self.hover else 'Stop recording\n(Double click)'
            self.configure(text=configure_text)
            self.after(100, self.update_timer)
