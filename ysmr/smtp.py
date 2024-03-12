import smtplib, ssl
from email.mime.text import MIMEText

def run(settings, log):
    # Set body
    message = f"{log.status} login at {log.timestamp} from {log.ipv4} on port {log.port}."
    msg = MIMEText(message)
    msg["Subject"] = f"{log.status} SSH Login"
    msg["From"] = settings["from"]

    # Initiate SSL
    context = ssl.create_default_context()

    # Login and send email
    with smtplib.SMTP_SSL(settings["server"], settings["port"], context=context) as server:
        server.login(settings["login"], settings["secret"])
        server.sendmail(settings["from"], settings["to"], msg.as_string())
    