"""Twilio SendGrid SMS notification module."""

from twilio.rest import Client


def run(conf, log):
    """Send SMS via Twilio SendGrid Rest API."""
    msg = (f"{log.timestamp} | {log.status} login from "
           f"{log.ipv4} on port {log.port}.")
    client = Client(conf.account_sid, conf.auth_token)
    message = client.messages \
                    .create(
                        body=msg,
                        from_=conf.sender,
                        to=conf.recipient
                    )
    # Send SMS
    print(message.sid)
