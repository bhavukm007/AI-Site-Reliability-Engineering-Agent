from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent import run_agent
import os   # ✅ ADD THIS

app = FastAPI()

class LogInput(BaseModel):
    logs: str

@app.get("/")
def home():
    return {"message": "AI SRE Agent Running"}

@app.post("/analyze")
def analyze_logs(data: LogInput):
    return run_agent(data.logs)

# ✅ ADD THIS NEW ENDPOINT BELOW
@app.get("/auto-analyze")
def auto_analyze():
    logs = ""

    for file in os.listdir("logs"):
        with open(f"logs/{file}", "r") as f:
            logs += f.read() + "\n"

    return run_agent(logs)
@app.post("/reset")
def reset_env():
    return {"status": "ok"}