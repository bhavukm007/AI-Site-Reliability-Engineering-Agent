# env/state.py

class SREState:
    def __init__(self, logs):
        self.original_logs = logs
        self.logs = logs
        self.status = "unresolved"
        self.resolved_errors = []

    # 🔹 UPDATE STATE BASED ON ACTION
    def update_state(self, action, errors):
        new_logs = []

        for error in errors:
            error_lower = error.lower()

            # Fix database errors
            if "database" in error_lower and action == "restart_db":
                self.resolved_errors.append(error)
                continue

            # Fix timeout errors
            elif "timeout" in error_lower and action == "scale_service":
                self.resolved_errors.append(error)
                continue

            # Fix generic failures
            elif action == "restart_service":
                self.resolved_errors.append(error)
                continue

            else:
                new_logs.append(error)

        # Update logs
        self.logs = "\n".join(new_logs)

        # Update system status
        if len(new_logs) == 0:
            self.status = "resolved"
        else:
            self.status = "unresolved"

    # 🔹 CHECK IF FULLY RESOLVED
    def is_resolved(self):
        return self.status == "resolved"