import tkinter
import customtkinter as ctk
from common.path_manager import PathManager
from common.button import Button
from common import variables

from controller.send_report import send_report
class SendReport(Button):
    def __init__(self, parent):
        super().__init__(parent, width=int(parent.x_width / 4) - 2, text='Wyślij raport', command=self.send_report)
        self.parent = parent
        self.mails: ctk.CTkToplevel

    def send_report(self):
        def send():
            mails_to_send_to = mails_var.get("1.0", "end-1c").split('\n')
            self.mails.destroy()
            with open(str(PathManager().cache / 'mails.txt'), 'w') as f:
                f.writelines('\n'.join(mails_to_send_to))

            trace_id = variables.display.trace_add('write', self.update_progress)
            try:
                send_report(variables.report_id.get(), mails_to_send_to)
            except Exception as e:
                variables.display.set(str(e))
            variables.display.trace_remove('write', trace_id)

        self.mails = ctk.CTkToplevel(self, height=self.parent.y_height * 10, width=int(self.parent.x_width / 2))
        self.mails.geometry(f'{int(self.parent.x_width / 2)}x{int(self.parent.y_height * 2)}')
        self.mails.title = ''

        mails_var = ctk.CTkTextbox(self.mails)
        start_text = open(str(PathManager().get_cache_file()), 'r').read() if PathManager().get_cache_file() else "Wpisz maile do których chcesz wysłać raport. Odziel kolejne adresy enterem"
        mails_var.insert("1.0", start_text)

        def clear_placeholder(event):
            if mails_var.get("1.0",
                             "end-1c") == "Wpisz maile do których chcesz wysłać raport. Odziel kolejne adresy enterem":
                mails_var.delete("1.0", "end")

        Button(self.mails, command=send, text='Wyślij').pack(side='bottom', anchor='center', expand=True)
        mails_var.pack(fill='both', expand=True)
        mails_var.bind("<FocusIn>", clear_placeholder)

    def update_progress(self, *args):
        self.parent.display.configure(text=f'Wysyłanie raportu: {variables.display.get()}')