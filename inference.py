import requests
import os
from openai import OpenAI

BASE_URL = "http://localhost:8000"

client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)


def log_start(task):
    print(f"[START] task={task} env=email-env model={os.environ.get('MODEL_NAME', 'unknown')}")


def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


def get_action_from_llm(observation):
    prompt = f"""
You are an email assistant.

Given emails:
{observation}

Choose:
- classify
- reply
- ignore

Return ONLY JSON:
{{"email_id": 1, "action_type": "classify", "response": ""}}
"""

    response = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": "You are an intelligent email assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return eval(content)
    except:
        return {"email_id": 1, "action_type": "classify", "response": ""}


def run():
    log_start("easy")

    res = requests.post(f"{BASE_URL}/reset").json()

    rewards = []
    steps = 0

    observation = res["observation"]

    for i in range(5):

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