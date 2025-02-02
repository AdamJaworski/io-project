import smtplib
import os
from common import variables
class Email:
    def __init__(self):
        self.mail = 'apikey'
        self.mail2 = os.getenv('SENDGRID_MAIL')
        self.password = os.getenv('SENDGRID')

        self.rec = os.getenv('SENDGRID2')
    def send_message(self, msg):
        try:
            with smtplib.SMTP('smtp.sendgrid.net', 587) as server:
                server.starttls()  # Ustawienie szyfrowania
                server.login(self.mail, self.password)
                server.send_message(msg)
                variables.display.set("Wiadomość wysłana pomyślnie!")
        except Exception as e:
            variables.display.set(f"Nie udało się wysłać wiadomości: {e}")

print(f"SENDGRID_MAIL: {os.getenv('SENDGRID_MAIL')}")
print(f"SENDGRID: {os.getenv('SENDGRID')}")
print(f"SENDGRID2: {os.getenv('SENDGRID2')}")