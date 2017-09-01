import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os

# username or passwd is invalid, change it to your correct mail info
EMAILFROM = 'user@qq.com'
EMAILTO = 'user@qq.com'
PASSWORD = 'password or auth_code'
SMTP_SERVER = 'smtp.qq.com:587'


def loign_and_send_mail(msg_to_send):
    print msg_to_send
    try:
        server = smtplib.SMTP(SMTP_SERVER)
        server.starttls()   # establish ssl connection
        server.login(EMAILFROM, PASSWORD)
        server.sendmail(EMAILFROM, EMAILTO, msg_to_send.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print 'error', e


def mail_content(fileToSend = None):
    msg = MIMEMultipart()
    msg["From"] = EMAILFROM
    msg["To"] = EMAILTO
    msg["Subject"] = "Check ping report"
    msg.preamble = "Check ping report"

    if not fileToSend:
        text_part = MIMEText('ping report not found, please check', 'plain', 'utf-8')
        return msg
    else:
        content_type, encoding = mimetypes.guess_type(fileToSend)
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        maintype, subtype = content_type.split("/", 1)
        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
        if not content_type.startswith("text/"):
            encoders.encode_base64(msg)
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment",
                              filename=fileToSend)
        text_part = MIMEText('ping report, please see it', 'plain', 'utf-8')
        msg.attach(text_part)
        msg.attach(attachment)
        return msg

def check_report_file():
    to_be_check_file = r'C:\Users\admin\Desktop\report.txt'
    if os.path.isfile(to_be_check_file):
        return to_be_check_file
    else:
        print "no report file"


if __name__ == "__main__":
    file = check_report_file()
    content_to_send = mail_content(file)
    loign_and_send_mail(content_to_send)
