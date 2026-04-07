# env/sre_env.py

from agent.log_parser import parse_logs
from agent.actions import execute_action

from env.state import SREState
from env.reward import calculate_reward
from env.tasks import get_task_logs

# 🆕 NEW IMPORTS
from env.schemas import SREObservation, SREAction, SREResult
from env.grader import is_success


class SREEnv:
    def __init__(self, task="easy"):
        self.task = task
        self.state_obj = None
        self.current_step = 0
        self.max_steps = 5

    # 🔹 RESET ENVIRONMENT
    def reset(self):
        log_text = get_task_logs(self.task)

        self.state_obj = SREState(log_text)
        self.current_step = 0

        # ✅ RETURN TYPED OBSERVATION
        return SREObservation(
            logs=self.state_obj.logs,
            status=self.state_obj.status
        )

    # 🔹 STEP FUNCTION
    def step(self, action_input):
        """
        action_input can be:
        - string (from your current system)
        - or SREAction (OpenEnv format)
        """

        self.current_step += 1

        # 🔹 HANDLE BOTH INPUT TYPES
        if isinstance(action_input, SREAction):
            action = action_input.action
        else:
            action = action_input

        # 🔹 Parse logs
        errors = parse_logs(self.state_obj.logs)

        # 🔹 Execute action
        result = execute_action(action)

        # 🔹 Update state
        self.state_obj.update_state(action, errors)

        # 🔹 Calculate reward
        reward = calculate_reward(errors, action, self.state_obj)

        # 🔹 Check done
        done = is_success(self.state_obj) or self.current_step >= self.max_steps

        # ✅ RETURN TYPED RESULT
        return SREResult(
            observation=SREObservation(
                logs=self.state_obj.logs,
                status=self.state_obj.status
            ),
            reward=reward,
            done=done,
            info={
                "action_result": result
            }
        )