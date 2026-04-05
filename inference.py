import requests
import random

BASE_URL = "http://localhost:8000"


def log_start(task):
    print(f"[START] task={task} env=email-env model=baseline")


def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null")


def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")


def safe_post(url, payload):
    """Safe request handler to avoid JSON crash"""
    try:
        response = requests.post(url, json=payload)

        # Debug print (VERY IMPORTANT)
        if response.status_code != 200:
            print("ERROR STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)
            return None

        return response.json()

    except Exception as e:
        print("REQUEST ERROR:", str(e))
        return None


def run():
    log_start("easy")

    # RESET
    res = safe_post(f"{BASE_URL}/reset", {})

    if res is None:
        print("[END] success=false steps=0 score=0.00 rewards=")
        return

    rewards = []
    steps = 0

    for i in range(5):
        action_type = random.choice(["classify", "reply", "ignore"])

        action = {
            "email_id": random.randint(1, 3),
            "action_type": action_type,
            "response": "Thank you for your email. We will resolve your issue shortly."
                        if action_type == "reply" else ""
        }

        res = safe_post(f"{BASE_URL}/step", action)

        if res is None:
            log_step(steps + 1, action_type, 0.0, True)
            break

        reward = res.get("reward", 0.0)
        done = res.get("done", False)

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