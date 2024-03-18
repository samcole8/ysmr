"""Telegram bot notification module for ysmr.

This module accepts the log and instance objects created by ysmr.

Using API parameters provided in the instance object, the log data is
wrapped in an API call and sent to Telegram accordingly.

This module is packaged by default with ysmr.
"""

import requests


def run(inst, log):
    """Post Telegram bot API call."""
    requests.post(f"https://api.telegram.org/bot{inst.bot_token}/sendMessage",
                  params={"chat_id": inst.chat_id, "text": log.get_msg()},)
