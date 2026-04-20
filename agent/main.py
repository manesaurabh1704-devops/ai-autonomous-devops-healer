from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import json
from agent.agent_core import run_agent

app = FastAPI(
    title="AI Autonomous DevOps Healer",
    description="AI Agent that heals Kubernetes clusters",
    version="1.0.0"
)

class Alert(BaseModel):
    alerts: list
    version: Optional[str] = "4"

class ManualRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "healthy", "agent": "ai-autonomous-devops-healer"}

@app.post("/webhook")
async def receive_alert(alert: Alert, background_tasks: BackgroundTasks):
    for a in alert.alerts:
        alert_name = a.get("labels", {}).get("alertname", "Unknown")
        pod_name = a.get("labels", {}).get("pod", "Unknown")
        severity = a.get("labels", {}).get("severity", "Unknown")
        status = a.get("status", "firing")

        if status == "firing":
            message = f"""
            ALERT RECEIVED:
            Alert: {alert_name}
            Pod: {pod_name}
            Severity: {severity}

            Please investigate and fix this issue.
            Get pod logs, analyze them, identify root cause,
            and take appropriate action.
            """
            background_tasks.add_task(run_agent, message)

    return {"status": "Alert received, agent activated"}

@app.post("/analyze")
async def manual_analyze(request: ManualRequest):
    result = run_agent(request.message)
    return {"result": result}

@app.get("/")
def root():
    return {
        "name": "AI Autonomous DevOps Healer",
        "status": "running",
        "endpoints": ["/health", "/webhook", "/analyze"]
    }
