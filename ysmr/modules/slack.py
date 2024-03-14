"""Slack notification module for ysmr.

This module accepts the log and config objects created by ysmr. Data from the
log object is converted into a readable message using a built-in method.

Using API parameters provided in the config object, the message is
wrapped in an API call and sent to Slack accordingly.

This module is packaged by default with ysmr.
"""
