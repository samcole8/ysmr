from twilio.rest import Client

def run(settings, log):
    msg = f"{log.timestamp} | {log.status} login from {log.ipv4} on port {log.port}."
    client = Client(settings["account_sid"], settings["auth_token"])
    message = client.messages \
                    .create(
                        body=msg,
                        from_=settings["from"],
                        to=settings["to"]
                    )
    # Send SMS
    print(message.sid)