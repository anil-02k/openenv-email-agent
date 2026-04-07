import requests
import os
from openai import OpenAI

# ✅ HF SPACE URL
BASE_URL = os.getenv(
    "BASE_URL",
    "https://anil2k47-email-triage-openenv.hf.space"
)

# ✅ ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("API_KEY")

# ✅ OPENAI CLIENT
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


# ✅ SAFE REQUEST
def safe_post(url, payload):
    try:
        res = requests.post(url, json=payload, timeout=10)

        if res.status_code != 200:
            return None

        return res.json()

    except Exception:
        return None


# ✅ SAFE LLM CALL (CRITICAL FIX)
def get_action_from_llm(observation):
    try:
        prompt = f"""
You are an email assistant.

Observation:
{observation}

Return STRICT JSON:
{{"email_id": 1, "action_type": "classify", "response": ""}}
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Email assistant"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content

        # ✅ SAFE PARSING
        try:
            return eval(content)
        except:
            return {"email_id": 1, "action_type": "classify", "response": ""}

    except Exception:
        # ✅ FALLBACK IF API FAILS
        return {"email_id": 1, "action_type": "classify", "response": ""}


# ✅ LOGS (STRICT FORMAT)
def log_start(task):
    print(f"[START] task={task} env=email-env model={MODEL_NAME}")


def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


# ✅ MAIN RUN
def run():
    try:
        log_start("easy")

        res = safe_post(f"{BASE_URL}/reset", {})

        if res is None:
            log_end(False, 0, 0.0, [])
            return

        observation = res.get("observation", {})

        rewards = []
        steps = 0

        for _ in range(5):

            action = get_action_from_llm(observation)

            res = safe_post(f"{BASE_URL}/step", action)

            if res is None:
                break

            reward = res.get("reward", 0.0)
            done = res.get("done", False)
            observation = res.get("observation", {})

            rewards.append(reward)
            steps += 1

            log_step(steps, action["action_type"], reward, done)

            if done:
                break

        score = min(1.0, sum(rewards) / max(1, len(rewards)))
        success = score > 0.3

        log_end(success, steps, score, rewards)

    except Exception:
        # ✅ FINAL FAILSAFE (IMPORTANT)
        log_end(False, 0, 0.0, [])


if __name__ == "__main__":
    run()