"""Twilio SendGrid notification module for ysmr.

This module accepts the log and config objects created by ysmr.

Using parameters provided in the config object, the log data is
wrapped in an API call and sent to Twilio SendGrid accordingly.

This module is packaged by default with ysmr.
"""

from twilio.rest import Client


def run(conf, log):
    """Send SMS via Twilio SendGrid Rest API."""
    client = Client(conf.account_sid, conf.auth_token)
    message = client.messages \
                    .create(
                        body=log.get_msg(),
                        from_=conf.sender,
                        to=conf.recipient
                    )
    # Send SMS
    print(message.sid)
