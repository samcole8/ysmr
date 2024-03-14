"""Local logging module for ysmr.

This module accepts the log and config objects created by ysmr.

The log data is converted to a readable format with the log's built-in method,
and written to a log file.

This module is packaged by default with ysmr.
"""

def run(settings, log):
    """Write log message to local filesystem."""
    with open("ysmr.log", "a") as f:
        f.write(log.get_msg())
