"""Local filesystem logging module."""

def run(settings, log):
    """Write log message to local filesystem."""
    with open("ysmr.log", "a") as f:
        f.write(log.get_msg())
