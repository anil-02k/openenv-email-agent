from fastapi import FastAPI
from server.environment import EmailEnv
from server.models import Action

app = FastAPI()
env = EmailEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict(),
        "reward": 0.0,
        "done": False
    }

@app.post("/step")
def step(action: Action):
    obs, reward, done, _ = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done
    }

# TEMPORARY SAFE MODE
def state(self):
    return {
        "steps": self.steps,
        "processed": self.processed,
        "correct": self.correct,
        "total_reward": self.total_reward
    }
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
