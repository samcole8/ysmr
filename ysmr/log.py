def run(settings, log):
    with open("ysmr.log", "a") as f:
        f.write(f"{log.timestamp} | {log.status} login from {log.ipv4} on port {log.port}.\n")