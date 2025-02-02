import customtkinter as ctk
from common import variables
from controller.send_report import send_report
from common.button import Button

class SendReport(Button):
    def __init__(self, parent):
        super().__init__(parent, width=int(parent.x_width / 4) - 2, text='Wyślij raport', command=self.send_report)
        self.parent = parent

    @staticmethod
    def send_report():
        send_report(variables.report_id, ['ajaworski@student.agh.edu.pl']) #TODO

