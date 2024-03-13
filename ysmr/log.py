"""Local filesystem logging module."""

def run(settings, log):
    """Write log message to local filesystem."""
    with open("ysmr.log", "a") as f:
        f.write(f"{log.timestamp} | {log.status} "
                f"login from {log.ipv4} on port {log.port}.\n")
