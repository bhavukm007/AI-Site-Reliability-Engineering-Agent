def execute_action(action):
    if action == "restart_db":
        return "Database restarted"
    elif action == "scale_service":
        return "Service scaled up"
    elif action == "restart_service":
        return "Service restarted"
    return "No action"