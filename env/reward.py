# env/reward.py

def calculate_reward(previous_errors, action, state_obj):
    total_errors = len(previous_errors)
    resolved_errors = len(state_obj.resolved_errors)

    # 🔹 CASE 1: No errors initially
    if total_errors == 0:
        return 1.0

    # 🔹 CASE 2: Progress-based reward
    progress = resolved_errors / total_errors

    # 🔹 BASE REWARD (partial credit)
    reward = progress

    # 🔹 BONUS for correct action types
    correct = False
    for error in previous_errors:
        e = error.lower()
        if "database" in e and action == "restart_db":
            correct = True
        elif "timeout" in e and action == "scale_service":
            correct = True
        elif action == "restart_service":
            correct = True

    if correct:
        reward += 0.2
    else:
        reward -= 0.2

    # 🔹 FINAL CLAMP (VERY IMPORTANT)
    reward = max(0.0, min(1.0, reward))

    return round(reward, 2)