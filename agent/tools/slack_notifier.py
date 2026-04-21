import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_slack_notification(message: str, status: str = "info") -> str:
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    if not webhook_url:
        return "Slack webhook not configured"

    emoji = {
        "success": ":white_check_mark:",
        "error": ":x:", 
        "warning": ":warning:",
        "info": ":information_source:",
        "healing": ":wrench:"
    }.get(status, ":information_source:")

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} AI DevOps Healer Alert"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            },
            {
                "type": "divider"
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            return "Slack notification sent successfully!"
        else:
            return f"Slack error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
