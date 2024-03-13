import requests

def run(conf, log):
    message=f"{log.status} login at {log.timestamp} from {log.ipv4} on port {log.port}.\n"
    requests.post(f"https://api.telegram.org/bot{conf.bot_token}/sendMessage", params={"chat_id": conf.chat_id, "text": message},)