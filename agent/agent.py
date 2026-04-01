from agent.log_parser import parse_logs
from agent.decision_engine import decide_action
from agent.actions import execute_action


def run_agent(log_text):
    errors = parse_logs(log_text)
    decision = decide_action(errors)
    result = execute_action(decision)

    return {
        "errors": errors,
        "decision": decision,
        "action_result": result
    }