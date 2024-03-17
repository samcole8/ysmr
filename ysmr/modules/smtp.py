"""SMTP notification module for ysmr.

This module accepts the log and config objects created by ysmr.

Using parameters provided in the config object, the log data is
wrapped in an API call and sent to an SMTP server.

This module is packaged by default with ysmr.
"""

import smtplib
import ssl
from email.mime.text import MIMEText


def run(conf, log):
    """Run the email notification process."""
    # Set body
    msg = MIMEText(log.get_msg())
    if log.status is None:
        msg["Subject"] = "SSH activity"
    else:
        msg["Subject"] = f"{log.status} SSH Login"
    msg["From"] = conf.sender

    # Initiate SSL
    context = ssl.create_default_context()

    # Login and send email
    with smtplib.SMTP_SSL(conf.server, conf.port, context=context) as server:
        server.login(conf.login, conf.secret)
        server.sendmail(conf.sender, conf.recipient, msg.as_string())
