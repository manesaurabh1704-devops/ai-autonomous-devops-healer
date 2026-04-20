from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from dotenv import load_dotenv
from agent.tools.k8s_healer import (
    get_pod_logs, restart_pod,
    get_all_pods, rollback_deployment
)
from agent.tools.prometheus_fetcher import (
    get_pod_restarts, get_pod_status
)
from agent.tools.log_analyzer import analyze_logs
import os

load_dotenv()

@tool
def tool_get_all_pods(namespace: str = "default") -> str:
    """Get all pods and their status in a namespace"""
    return get_all_pods(namespace)

@tool
def tool_get_pod_logs(pod_name: str) -> str:
    """Get logs of a specific pod by name"""
    return get_pod_logs(pod_name)

@tool
def tool_restart_pod(pod_name: str) -> str:
    """Restart a specific pod by name"""
    return restart_pod(pod_name)

@tool
def tool_rollback_deployment(deployment_name: str) -> str:
    """Rollback a deployment to previous version"""
    return rollback_deployment(deployment_name)

@tool
def tool_get_pod_restarts(pod_name: str) -> str:
    """Get restart count of a pod from Prometheus"""
    return get_pod_restarts(pod_name)

@tool
def tool_analyze_logs(logs: str) -> str:
    """Analyze logs and identify issues"""
    return analyze_logs(logs)

def create_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    tools = [
        tool_get_all_pods,
        tool_get_pod_logs,
        tool_restart_pod,
        tool_rollback_deployment,
        tool_get_pod_restarts,
        tool_analyze_logs
    ]

    system_prompt = """You are an expert DevOps AI agent.
    Your job is to:
    1. Analyze Kubernetes alerts and failures
    2. Get pod logs and metrics
    3. Identify root cause of issues
    4. Take corrective actions (restart pods, rollback deployments)
    5. Provide clear summary of what happened and what you did

    Always be concise and action-oriented.
    After fixing, summarize: Problem → Root Cause → Action Taken → Result
    """

    agent = create_react_agent(
        llm,
        tools,
        prompt=system_prompt
    )
    return agent

def run_agent(alert_message: str) -> str:
    try:
        agent = create_agent()
        result = agent.invoke({"messages": [("human", alert_message)]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Agent error: {str(e)}"
