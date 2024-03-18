"""Twilio SendGrid notification module for ysmr.

This module accepts the log and instig objects created by ysmr.

Using parameters provided in the instig object, the log data is
wrapped in an API call and sent to Twilio SendGrid accordingly.

This module is packaged by default with ysmr.
"""

from twilio.rest import Client


def run(inst, log):
    """Send SMS via Twilio SendGrid Rest API."""
    client = Client(inst.account_sid, inst.auth_token)
    message = client.messages \
                    .create(
                        body=log.get_msg(),
                        from_=inst.sender,
                        to=inst.recipient
                    )
    # Send SMS
    print(message.sid)
