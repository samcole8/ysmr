"""Telegram Bot notification module."""

import requests


def run(conf, log):
    """Post Telegram bot API call."""
    msg = (f"{log.timestamp} | {log.status} login from "
           f"{log.ipv4} on port {log.port}.")
    requests.post(f"https://api.telegram.org/bot{conf.bot_token}/sendMessage",
                  params={"chat_id": conf.chat_id, "text": msg},)
