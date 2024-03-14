"""Telegram bot notification module for ysmr.

This module accepts the log and config objects created by ysmr.

Using API parameters provided in the config object, the log data is
wrapped in an API call and sent to Telegram accordingly.

This module is packaged by default with ysmr.
"""

import requests


def run(conf, log):
    """Post Telegram bot API call."""
    requests.post(f"https://api.telegram.org/bot{conf.bot_token}/sendMessage",
                  params={"chat_id": conf.chat_id, "text": log.get_msg()},)
