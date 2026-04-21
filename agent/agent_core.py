from langchain_aws import ChatBedrock
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
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
from agent.tools.slack_notifier import send_slack_notification
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

@tool
def tool_send_slack_notification(message: str, status: str = "info") -> str:
    """Send notification to Slack #alerts channel"""
    return send_slack_notification(message, status)

def get_llm():
    # Production → AWS Bedrock Claude Haiku
    # Development → Groq Llama
    use_bedrock = os.getenv("USE_BEDROCK", "false").lower() == "true"

    if use_bedrock:
        return ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name=os.getenv("AWS_REGION", "ap-south-1"),
            model_kwargs={"temperature": 0}
        )
    else:
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )

def create_agent():
    llm = get_llm()

    tools = [
        tool_get_all_pods,
        tool_get_pod_logs,
        tool_restart_pod,
        tool_rollback_deployment,
        tool_get_pod_restarts,
        tool_analyze_logs,
        tool_send_slack_notification
    ]

    system_prompt = """You are an expert DevOps AI agent.
    Your job is to:
    1. Analyze Kubernetes alerts and failures
    2. Get pod logs and metrics
    3. Identify root cause of issues
    4. Take corrective actions (restart pods, rollback deployments)
    5. Send Slack notifications about what happened
    6. Provide clear summary: Problem → Root Cause → Action → Result

    ALWAYS send a Slack notification after taking any action.
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
