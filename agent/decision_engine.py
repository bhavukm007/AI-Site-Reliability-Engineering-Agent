def decide_action(errors):
    if not errors:
        return "No issues detected"

    if any("database" in e.lower() for e in errors):
        return "restart_db"
    elif any("timeout" in e.lower() for e in errors):
        return "scale_service"
    else:
        return "restart_service"