"""SMTP notification module for ysmr.

This module accepts the log and instance objects created by ysmr.

Using parameters provided in the instance object, the log data is
wrapped in an API call and sent to an SMTP server.

This module is packaged by default with ysmr.
"""

import smtplib
import ssl
from email.mime.text import MIMEText


def run(inst, log):
    """Run the email notification process."""
    # Set body
    msg = MIMEText(log.get_msg())
    if log.status is None:
        msg["Subject"] = "SSH activity"
    else:
        msg["Subject"] = f"{log.status} SSH Login"
    msg["From"] = inst.sender

    # Initiate SSL
    context = ssl.create_default_context()

    # Login and send email
    with smtplib.SMTP_SSL(inst.server, inst.port, context=context) as server:
        server.login(inst.login, inst.secret)
        server.sendmail(inst.sender, inst.recipient, msg.as_string())
