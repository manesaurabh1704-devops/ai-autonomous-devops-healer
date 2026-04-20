from kubernetes import client, config

def load_k8s_config():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()

def get_pod_logs(pod_name: str, namespace: str = "default") -> str:
    try:
        load_k8s_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace=namespace)
        for pod in pods.items:
            if pod_name.lower() in pod.metadata.name.lower():
                logs = v1.read_namespaced_pod_log(
                    name=pod.metadata.name,
                    namespace=namespace,
                    tail_lines=50
                )
                return f"Pod: {pod.metadata.name}\nLogs:\n{logs}"
        return f"Pod {pod_name} not found"
    except Exception as e:
        return f"Error getting logs: {str(e)}"

def restart_pod(pod_name: str, namespace: str = "default") -> str:
    try:
        load_k8s_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace=namespace)
        for pod in pods.items:
            if pod_name.lower() in pod.metadata.name.lower():
                v1.delete_namespaced_pod(
                    name=pod.metadata.name,
                    namespace=namespace
                )
                return f"✅ Pod {pod.metadata.name} restarted!"
        return f"Pod {pod_name} not found"
    except Exception as e:
        return f"Error restarting pod: {str(e)}"

def get_all_pods(namespace: str = "default") -> str:
    try:
        load_k8s_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace=namespace)
        result = []
        for pod in pods.items:
            result.append(
                f"{pod.metadata.name} → {pod.status.phase}"
            )
        return "\n".join(result)
    except Exception as e:
        return f"Error getting pods: {str(e)}"

def rollback_deployment(deployment_name: str, namespace: str = "default") -> str:
    try:
        load_k8s_config()
        apps_v1 = client.AppsV1Api()
        import datetime
        body = {
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kubectl.kubernetes.io/restartedAt": 
                            datetime.datetime.now().isoformat()
                        }
                    }
                }
            }
        }
        apps_v1.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=body
        )
        return f"✅ Deployment {deployment_name} rollback triggered!"
    except Exception as e:
        return f"Error rolling back: {str(e)}"
