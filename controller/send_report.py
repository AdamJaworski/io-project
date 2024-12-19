import os
from model.send_report import Email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from common.path_manager import PathManager

email_ = Email()

def send_report(report_id, to):
    msg = MIMEMultipart()
    msg['From'] = email_.mail2
    msg['To'] = ', '.join(to)
    msg['Subject'] = 'Raport ze spotkania'

    report_path = PathManager(report_id).get_report_path()
    report = None
    for file in os.listdir(report_path):
        if file.split('.')[-1] == 'pdf':
            report = file
            break

    with open(str(report_path / report), 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(f'Content-Disposition', f'attachment; filename="{report}"')
        msg.attach(part)

    email_.send_message(msg)