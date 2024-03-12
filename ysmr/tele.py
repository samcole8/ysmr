import requests

def run(settings, log):
    message=f"{log.status} login at {log.timestamp} from {log.ipv4} on port {log.port}.\n"
    requests.post(f"https://api.telegram.org/bot{settings['bot_token']}/sendMessage", params={"chat_id": settings["chat_id"], "text": message},)