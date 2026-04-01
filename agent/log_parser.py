import re

def parse_logs(log_text):
    errors = []
    for line in log_text.split("\n"):
        if "ERROR" in line or "CRITICAL" in line:
            errors.append(line)
    return errors