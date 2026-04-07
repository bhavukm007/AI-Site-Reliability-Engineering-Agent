import os
from openai import OpenAI

from env.sre_env import SREEnv
from env.grader import calculate_score


API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")

API_KEY = (
    os.getenv("OPENAI_API_KEY")
    or os.getenv("HF_TOKEN")
    or os.getenv("API_KEY")
)

print("API_KEY loaded:", API_KEY is not None)

TASK_NAME = os.getenv("TASK_NAME", "easy")
MAX_STEPS = 5

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


# 🔹 LOG FORMAT FUNCTIONS (STRICT FORMAT)
def log_start():
    print(f"[START] task={TASK_NAME} env=sre_env model={MODEL_NAME}", flush=True)


def log_step(step, action, reward, done, error=None):
    error_val = error if error else "null"
    done_val = str(done).lower()

    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# 🔹 LLM DECISION
def get_action_from_model(logs):
    prompt = f"""
    You are an SRE agent. Based on logs, choose ONE action:
    restart_db, scale_service, restart_service

    Logs:
    {logs}

    Only return the action name.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0
        )

        action = response.choices[0].message.content.strip()
        return action

    except Exception as e:
        return "restart_service"


# 🔹 MAIN LOOP
def main():
    env = SREEnv(task=TASK_NAME)

    rewards = []
    steps_taken = 0

    log_start()

    try:
        observation = env.reset()

        for step in range(1, MAX_STEPS + 1):

            logs = observation.logs

            action = get_action_from_model(logs)

            result = env.step(action)

            reward = result.reward
            done = result.done

            rewards.append(reward)
            steps_taken = step

            log_step(step, action, reward, done)

            observation = result.observation

            if done:
                break

        # 🔹 SCORE USING GRADER
        score = calculate_score(env.state_obj, steps_taken, MAX_STEPS)

        success = score >= 0.5

    except Exception as e:
        success = False
        score = 0.0

    finally:
        log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    main()