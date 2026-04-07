# env/tasks.py

from scenarios.bad_commit import simulate as bad_commit_sim
from scenarios.cascading_failure import simulate as cascading_sim


# 🔹 DEFINE TASK LOGS
def get_task_logs(task_name):
    
    if task_name == "easy":
        # Single issue (database failure)
        return "ERROR: database connection failed"

    elif task_name == "medium":
        # Two issues (database + timeout)
        return (
            "ERROR: database connection failed\n"
            "ERROR: timeout occurred"
        )

    elif task_name == "hard":
        # Multiple cascading failures
        return cascading_sim()

    elif task_name == "bad_commit":
        return bad_commit_sim()

    else:
        # Default fallback
        return "ERROR: unknown system failure"