"""SMTP Email notification module."""

import smtplib
import ssl
from email.mime.text import MIMEText


def run(conf, log):
    """Run the email notification process."""
    # Set body
    msg = MIMEText(log.get_msg())
    msg["Subject"] = f"{log.status} SSH Login"
    msg["From"] = conf.sender

    # Initiate SSL
    context = ssl.create_default_context()

    # Login and send email
    with smtplib.SMTP_SSL(conf.server, conf.port, context=context) as server:
        server.login(conf.login, conf.secret)
        server.sendmail(conf.sender, conf.recipient, msg.as_string())
