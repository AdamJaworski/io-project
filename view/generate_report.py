import threading
from common import variables
from controller.generate_raport import generate_report
from model.generate_raport import Report
from common.button import Button

class GenerateReport(Button):
    def __init__(self, parent):
        super().__init__(parent, width=int(parent.x_width / 4) - 5, text='Stwórz raport', command=self.start_generating_report)

        self.parent = parent

    def start_generating_report(self):
        """We don't want report gen to freeze ui (stop main loop) so we need to gen report in new thread"""
        threading.Thread(target=self.generate_report).start()

    def generate_report(self):
        variables.display.trace_add('write', self.update_progress)
        generate_report(Report(variables.report_id))
        variables.display.trace_add('write', self.update_progress)

    def update_progress(self, *args):
        self.parent.display.configure(text=f'Tworzenie raportu: {variables.display.get()}')