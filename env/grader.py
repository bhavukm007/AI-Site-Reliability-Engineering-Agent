# env/grader.py

from agent.log_parser import parse_logs


# 🔹 CHECK IF TASK IS SUCCESSFUL
def is_success(state_obj):
    """
    Success = no remaining errors in logs
    """
    remaining_errors = parse_logs(state_obj.logs)
    return len(remaining_errors) == 0


# 🔹 CALCULATE FINAL SCORE (0 → 1)
def calculate_score(state_obj, steps_taken, max_steps):
    """
    Score logic:
    - Fully resolved → high score
    - Faster resolution → better score
    - Partial resolution → partial score
    """

    total_initial_errors = len(parse_logs(state_obj.original_logs))
    remaining_errors = len(parse_logs(state_obj.logs))

    # 🔹 Edge case: no errors initially
    if total_initial_errors == 0:
        return 1.0

    # 🔹 Progress ratio
    resolved = total_initial_errors - remaining_errors
    progress_score = resolved / total_initial_errors

    # 🔹 Efficiency bonus (fewer steps = better)
    efficiency_bonus = (max_steps - steps_taken) / max_steps

    # 🔹 Final score
    score = 0.7 * progress_score + 0.3 * efficiency_bonus

    # 🔹 Clamp to [0, 1]
    score = max(0.0, min(1.0, score))

    return round(score, 2)