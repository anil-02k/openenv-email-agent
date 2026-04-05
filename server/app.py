from fastapi import FastAPI
from environment import EmailEnv
from models import Action

app = FastAPI()
env = EmailEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.dict(), "reward": 0.0, "done": False}

@app.post("/step")
def step(action: Action):
    obs, reward, done, _ = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done
    }

@app.get("/state")
def state():
    return {
        "steps": env.steps,
        "processed": env.processed,
        "total_reward": env.total_reward
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
