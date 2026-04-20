def analyze_logs(logs: str) -> str:
    issues = []

    patterns = {
        "OOMKilled": "Out of Memory — Container killed",
        "CrashLoopBackOff": "Pod crash looping",
        "ImagePullBackOff": "Cannot pull Docker image",
        "Connection refused": "Service connection refused",
        "OutOfMemoryError": "Java OOM — increase memory",
        "ERROR": "Application error detected",
        "FATAL": "Fatal error detected",
        "Exception": "Exception in application",
        "timeout": "Timeout detected",
        "permission denied": "Permission issue"
    }

    for pattern, description in patterns.items():
        if pattern.lower() in logs.lower():
            issues.append(f"⚠️  {pattern}: {description}")

    if not issues:
        return "✅ No critical issues found in logs"

    return "Issues Found:\n" + "\n".join(issues)
