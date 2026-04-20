from prometheus_api_client import PrometheusConnect
from dotenv import load_dotenv
import os

load_dotenv()

def get_prometheus_metrics(query: str) -> str:
    try:
        prom = PrometheusConnect(
            url=os.getenv("PROMETHEUS_URL"),
            disable_ssl=True
        )
        result = prom.custom_query(query=query)
        return str(result)
    except Exception as e:
        return f"Error fetching metrics: {str(e)}"

def get_pod_restarts(pod_name: str) -> str:
    query = f'kube_pod_container_status_restarts_total{{pod=~"{pod_name}.*"}}'
    return get_prometheus_metrics(query)

def get_pod_status() -> str:
    query = 'kube_pod_status_phase{namespace="default"}'
    return get_prometheus_metrics(query)
