"""Twilio SendGrid SMS notification module."""

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
