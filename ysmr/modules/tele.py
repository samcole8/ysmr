"""Telegram Bot notification module."""

import requests


def run(conf, log):
    """Post Telegram bot API call."""
    requests.post(f"https://api.telegram.org/bot{conf.bot_token}/sendMessage",
                  params={"chat_id": conf.chat_id, "text": log.get_msg()},)
