import requests
import os
from openai import OpenAI

BASE_URL = "http://localhost:8000"

# ✅ REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("API_KEY")  # ❗ NO DEFAULT

# ✅ OPENAI CLIENT (MANDATORY)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


def log_start(task):
    print(f"[START] task={task} env=email-env model={MODEL_NAME}")


def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


# ✅ LLM FUNCTION (CRITICAL)
def get_action_from_llm(observation):

    prompt = f"""
You are an AI email assistant.

Given the emails:
{observation}

Choose best action:
- classify
- reply
- ignore

Return STRICT JSON ONLY:
{{"email_id": 1, "action_type": "classify", "response": ""}}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an intelligent email assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        return eval(content)
    except:
        # fallback (safe)
        return {"email_id": 1, "action_type": "classify", "response": ""}


def run():
    log_start("easy")

    res = requests.post(f"{BASE_URL}/reset").json()

    observation = res["observation"]

    rewards = []
    steps = 0

    for i in range(5):

        # ✅ MUST USE LLM (NOT RANDOM)
        action = get_action_from_llm(observation)

        res = requests.post(f"{BASE_URL}/step", json=action).json()

        reward = res["reward"]
        done = res["done"]
        observation = res["observation"]

        rewards.append(reward)
        steps += 1

        log_step(steps, action["action_type"], reward, done)

        if done:
            break

    score = min(1.0, sum(rewards) / max(1, len(rewards)))
    success = score > 0.3

    log_end(success, steps, score, rewards)


if __name__ == "__main__":
    run()