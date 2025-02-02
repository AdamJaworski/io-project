from common import variables
import customtkinter as ctk

class Button(ctk.CTkButton):
    def __init__(self, master, command=None, text='', width=110, height=30):
        super().__init__(master,
                         width=width,
                         height=height,
                         command=command,
                         text=text,
                         corner_radius=5,
                         border_width=3,
                         fg_color=variables.BACKGROUND_MIDDLE,
                         hover_color=variables.BUTTON_HOVER,
                         text_color=variables.BUTTON_TEXT,
                         border_color=variables.BUTTON_BORDER
                         )
