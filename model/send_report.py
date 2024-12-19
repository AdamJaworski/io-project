import smtplib
import os

class Email:
    def __init__(self):
        self.mail = 'apikey'
        self.mail2 = 'ioprojectplaceholder@gmail.com'
        self.password = os.getenv('SENDGRID')

        self.rec = os.getenv('SENDGRID2')
    def send_message(self, msg):
        try:
            with smtplib.SMTP('smtp.sendgrid.net', 587) as server:
                server.starttls()  # Ustawienie szyfrowania
                server.login(self.mail, self.password)
                server.send_message(msg)
                print("Wiadomość wysłana pomyślnie!")
        except Exception as e:
            print(f"Nie udało się wysłać wiadomości: {e}")