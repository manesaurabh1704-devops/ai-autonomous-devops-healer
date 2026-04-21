# 🤖 ai-autonomous-devops-healer

<div align="center">

**An AI-powered autonomous agent that watches your Kubernetes cluster 24/7, detects pod failures, analyzes root cause using LLM, and self-heals — without any human intervention.**

![GitHub Actions](https://github.com/manesaurabh1704-devops/ai-autonomous-devops-healer/actions/workflows/ci-cd.yaml/badge.svg)
![AWS EKS](https://img.shields.io/badge/AWS-EKS-orange?logo=amazonaws)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20Bedrock-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.31-326CE5?logo=kubernetes)

</div>

---

## 📌 What Is This?

A production-grade **Agentic AI DevOps system** built on AWS EKS. When a pod crashes:

1. **Prometheus** detects the failure
2. **Alertmanager** fires a webhook
3. **FastAPI** receives the alert
4. **LangChain Agent** (powered by Groq/AWS Bedrock) analyzes logs and identifies root cause
5. **Agent self-heals** — restarts the pod or rolls back the deployment
6. **Slack** gets a full incident report

No pager alerts. No manual `kubectl` commands. Just autonomous healing.

---

## 🏗️ Architecture

```
                        ┌─────────────────────────────────────────────┐
                        │           AWS Mumbai (ap-south-1)            │
                        │                                              │
YOUR LAPTOP             │  PUBLIC SUBNET          PRIVATE SUBNET       │
    │                   │  ┌──────────────┐    ┌──────────────────┐   │
    │ VS Code SSH        │  │ Load Balancer│    │  EKS Cluster     │   │
    ▼                   │  │ React Frontend│    │  ┌────────────┐  │   │
EC2 Workstation         │  │ NAT Gateway  │    │  │  Backend   │  │   │
(Terraform runs here)   │  └──────────────┘    │  │  MariaDB   │  │   │
    │                   │         │             │  │  AI Agent  │  │   │
    │ terraform apply   │         │ Internal    │  │  Prometheus│  │   │
    ▼                   │         └────────────▶│  │  Grafana   │  │   │
Infra Created ──────────┘                       │  └────────────┘  │   │
                                                └──────────────────┘   │
                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Self-Healing Flow

```
Pod Crash
    │
    ▼
Prometheus detects
    │
    ▼
Alertmanager → Webhook
    │
    ▼
FastAPI Server
    │
    ▼
LangChain Agent
    ├── tool: get_pod_logs()
    ├── tool: get_prometheus_metrics()
    ├── tool: analyze_logs()
    └── tool: restart_pod() / rollback_deployment()
    │
    ▼
Slack #alerts → Incident Report
```

---

## 🛠️ Tech Stack

| Category | Tool | Purpose |
|---|---|---|
| **AI Agent** | LangChain + LangGraph | Agent orchestration |
| **LLM (Dev)** | Groq — Llama 3.3 70B | Free, fast development |
| **LLM (Prod)** | AWS Bedrock — Claude Haiku | Production, IAM auth |
| **API Server** | FastAPI + Uvicorn | Webhook receiver |
| **IaC** | Terraform Modules | Infrastructure as Code |
| **Cloud** | AWS ap-south-1 (Mumbai) | Cloud provider |
| **Container** | Docker (multi-stage) | Image build |
| **Orchestration** | AWS EKS — Kubernetes 1.31 | Container orchestration |
| **Monitoring** | Prometheus + Grafana | Metrics + dashboards |
| **Alerting** | Alertmanager | Alert routing |
| **Notification** | Slack Webhooks | Incident reporting |
| **CI/CD** | GitHub Actions | Automated deployments |
| **App** | StudentSphere (React + Spring Boot + MariaDB) | Target application |

---

## 🔐 Security Design

Backend, database, and AI agent are **completely isolated** from the internet:

```
PUBLIC SUBNET (Internet accessible):
├── Load Balancer          ← Users enter here
├── React Frontend         ← Served via nginx
└── NAT Gateway            ← Outbound only for private resources

PRIVATE SUBNET (No direct internet):
├── Spring Boot Backend    ← Only reachable from frontend
├── MariaDB Database       ← Only reachable from backend
├── AI Agent (FastAPI)     ← Only reachable from cluster
├── Prometheus             ← Internal metrics only
└── Grafana                ← Internal dashboards only
```

Security groups enforce these rules at the network level — not just application level.

---

## 📁 Repository Structure

```
ai-autonomous-devops-healer/
│
├── agent/                          # 🤖 Core AI Agent
│   ├── main.py                     # FastAPI — /health /webhook /analyze
│   ├── agent_core.py               # LangChain agent + Groq/Bedrock toggle
│   └── tools/
│       ├── k8s_healer.py           # Pod restart, rollback, log fetch
│       ├── log_analyzer.py         # Pattern matching on logs
│       ├── prometheus_fetcher.py   # Metrics queries
│       └── slack_notifier.py       # #alerts channel notifications
│
├── app/
│   ├── frontend/                   # React (StudentSphere)
│   └── backend/                    # Spring Boot (StudentSphere)
│
├── terraform/                      # Infrastructure as Code
│   ├── main.tf                     # Module calls only — clean root
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── vpc/                    # VPC + Subnets + IGW + NAT
│       ├── security_groups/        # LB, Frontend, Backend, DB SGs
│       ├── ec2/                    # Workstation instance
│       └── eks/                    # EKS Cluster + Node Group
│
├── k8s/
│   ├── app/                        # App manifests
│   │   ├── frontend.yaml
│   │   ├── backend.yaml
│   │   └── mariadb.yaml
│   └── agent/
│       └── deployment.yaml         # Agent + ServiceAccount + RBAC
│
├── monitoring/
│   ├── alert-rules.yaml            # Custom PrometheusRule
│   └── alertmanager-config.yaml    # Webhook to agent
│
├── .github/workflows/
│   └── ci-cd.yaml                  # Build → Push → Deploy pipeline
│
├── Dockerfile                      # Agent container
├── requirements.txt
├── .env.example
└── docs/screenshots/               # Phase-by-phase proof
```

---

## 📸 Project Walkthrough

### Phase 1 — Project Foundation

**What:** Created fresh GitHub repo, copied only application code (React + Spring Boot) from StudentSphere project.

**Why:** Clean slate — no legacy Terraform, K8s manifests, or CI/CD config from previous project. Everything built from scratch for this project.

**How:**
```bash
git clone https://github.com/manesaurabh1704-devops/ai-autonomous-devops-healer.git
cp -r ../multi-cloud-devops-studentsphere/frontend app/frontend
cp -r ../multi-cloud-devops-studentsphere/backend app/backend
```

---

### Phase 2 — AWS Infrastructure via Terraform Modules

**What:** Built production-grade AWS infrastructure using Terraform modules — Custom VPC, public/private subnets, Internet Gateway, NAT Gateway, Security Groups, EC2 workstation, and EKS cluster.

**Why:** Terraform modules make infrastructure reusable, testable, and version-controlled. Modules separate concerns — VPC logic doesn't mix with EKS logic.

**How:**
```bash
cd terraform
terraform init
terraform plan
terraform apply   # 23 resources created
```

![Terraform Apply Complete](docs/screenshots/01-terraform-apply.png)
![EC2 Instance Running](docs/screenshots/02-Running-instance.png)
![EKS Cluster Active](docs/screenshots/03-Cluster-active.png)
![kubectl get nodes](docs/screenshots/04-kubectl-get-nodes-output.png)

---

### Phase 3 — App Deployment on EKS

**What:** Dockerized StudentSphere (React + Spring Boot + MariaDB) with fresh multi-stage Dockerfiles and deployed to EKS via Kubernetes manifests.

**Why:** Multi-stage builds reduce image size significantly. Backend and database deployed in private subnet — not exposed to internet.

**How:**
```bash
# Build and push images
docker build -t manesaurabh1704devops/ai-healer-frontend:latest app/frontend/
docker build -t manesaurabh1704devops/ai-healer-backend:latest app/backend/

# Deploy to EKS
kubectl apply -f k8s/app/mariadb.yaml
kubectl apply -f k8s/app/backend.yaml
kubectl apply -f k8s/app/frontend.yaml
```

![App Live on EKS](docs/screenshots/05-Student-registered-successfully.png)

---

### Phase 4 — Monitoring Stack

**What:** Deployed Prometheus, Grafana, and Alertmanager using Helm (`kube-prometheus-stack`). Created custom alert rules for pod crashes, high CPU, and memory issues.

**Why:** Prometheus is the industry standard for Kubernetes monitoring. Custom alert rules ensure the AI agent gets triggered on real failures — not just default K8s alerts.

**How:**
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring

kubectl apply -f monitoring/alert-rules.yaml
kubectl apply -f monitoring/alertmanager-config.yaml
```

Custom alert rules created:
- `PodCrashLooping` — fires when pod restart rate > 0 for 1 minute
- `PodNotRunning` — fires when pod not in Running phase
- `HighCPUUsage` — fires when CPU > 80% for 2 minutes
- `HighMemoryUsage` — fires when memory > 80% for 2 minutes

![Monitoring Stack Running](docs/screenshots/06-monitoring-output.png)

---

### Phase 5 — AI Agent (LangChain + Groq)

**What:** Built a LangChain-powered AI agent with 6 tools: pod log fetcher, prometheus metrics, log analyzer, pod restarter, deployment rollback, and Slack notifier. Exposed via FastAPI.

**Why:** LangChain's tool-calling framework lets the LLM decide which tools to use based on the alert — making it truly autonomous. FastAPI provides a webhook endpoint for Alertmanager.

**How:**
```python
# Agent with 6 tools
agent = create_react_agent(llm, tools, prompt=system_prompt)

# Endpoints
GET  /health    → Agent status
POST /webhook   → Alertmanager webhook receiver
POST /analyze   → Manual trigger
```

```bash
uvicorn agent.main:app --host 0.0.0.0 --port 8000
```

![Agent Working](docs/screenshots/07-agent-working.png)
![FastAPI Health Check](docs/screenshots/08-fastapi-health.png)
![Uvicorn Server](docs/screenshots/09-uvicorn-running.png)
![Analyze Endpoint](docs/screenshots/10-agent-analyze-api.png)
![Self Healing Demo](docs/screenshots/11-self-healing-demo.png)

---

### Phase 6 — GitHub Actions CI/CD

**What:** Automated CI/CD pipeline triggered on every `main` branch push — builds Docker images, pushes to DockerHub, and deploys to EKS.

**Why:** Manual deployment is error-prone. Every code change should automatically reach production without human intervention.

**How:**
```yaml
# Pipeline steps
- Checkout Code
- Login to DockerHub
- Build + Push Frontend Image
- Build + Push Backend Image
- Configure AWS Credentials (IAM)
- Update kubeconfig
- Deploy to EKS
- Verify Deployment (rollout status)
```

![CI/CD Pipeline Success](docs/screenshots/12-cicd-success.png)
![CI/CD All Steps](docs/screenshots/13-cicd-steps.png)

---

### Phase 7 — Slack Notifications

**What:** AI agent sends structured incident reports to Slack `#alerts` channel via Incoming Webhooks — covering what happened, root cause, action taken, and result.

**Why:** DevOps teams need visibility into autonomous actions. Slack notifications ensure every self-healing action is logged and human-readable.

**How:**
```python
payload = {
    "blocks": [
        {"type": "header", "text": f"{emoji} AI DevOps Healer Alert"},
        {"type": "section", "text": message}
    ]
}
requests.post(webhook_url, json=payload)
```

![Slack Webhook Setup](docs/screenshots/14-slack-webhook-created.png)
![Slack Alerts Channel](docs/screenshots/15-slack-alerts-channel.png)
![Slack Notification Working](docs/screenshots/16-slack-notification-working.png)

---

### Phase 8 — Agent Deployed on Kubernetes

**What:** Packaged the AI agent as a Docker container and deployed it as a Kubernetes pod with proper RBAC (ServiceAccount + ClusterRole + ClusterRoleBinding).

**Why:** Running the agent inside the cluster it monitors is the production approach — lower latency, no external auth needed, and agent uses in-cluster K8s config automatically.

**How:**
```yaml
# Agent has only the permissions it needs
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "patch", "update"]
```

```bash
kubectl create secret generic ai-agent-secrets \
  --from-literal=GROQ_API_KEY=... \
  --from-literal=SLACK_WEBHOOK_URL=...

kubectl apply -f k8s/agent/deployment.yaml
```

![Agent Pod Running on EKS](docs/screenshots/17-agent-on-kubernetes.png)

---

### Phase 9 — AWS Bedrock Integration

**What:** Integrated AWS Bedrock (Claude Haiku) as the production LLM alongside Groq (development). A single environment variable switches between them.

**Why:** AWS Bedrock uses IAM role authentication — no API keys to manage. This is the production-grade approach for AWS-native deployments.

**How:**
```python
def get_llm():
    if os.getenv("USE_BEDROCK") == "true":
        return ChatBedrock(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            region_name="ap-south-1"
        )
    else:
        return ChatGroq(model="llama-3.3-70b-versatile")
```

```bash
# Switch to production LLM
USE_BEDROCK=true  # in .env or K8s secret
```

---

### Phase 10 — Grafana Dashboards

**What:** Imported Kubernetes pod monitoring dashboard (ID: 15760) into Grafana, showing CPU, memory, and pod health for all namespaces.

**Why:** Visual monitoring lets you spot trends before they become incidents. Grafana + Prometheus is the industry standard observability stack.

**How:**
```bash
# Expose Grafana via LoadBalancer
kubectl patch svc prometheus-grafana -n monitoring \
  -p '{"spec": {"type": "LoadBalancer"}}'
```

Dashboard shows:
- Pod CPU and memory usage per container
- Pod phase status
- Network I/O
- Resource requests vs limits

![Grafana Home](docs/screenshots/18-grafana-dashboard.png)
![Kubernetes Dashboard](docs/screenshots/19-grafana-kubernetes-dashboard.png)
![Default Namespace Pods](docs/screenshots/20-grafana-default-namespace.png)

---

### Phase 11 — Chaos Engineering Demo

**What:** Live end-to-end self-healing demonstration — deliberately crashed the backend pod and watched the AI agent detect, analyze, heal, and report.

**Why:** Chaos engineering is how you prove your resilience system actually works. Talk is cheap — screenshots and logs are proof.

**How — Full Demo:**

```bash
# Terminal 1: Agent server running
uvicorn agent.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Live pod watch
watch -n 2 kubectl get pods

# Terminal 3: Inject chaos
kubectl delete pod -l app=backend

# Trigger agent
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "CRITICAL: Backend pod crashed! Check logs, identify root cause, restart and send Slack report"}'
```

**Agent Response:**
```
Problem    → Backend pod has crashed!
Root Cause → No critical issues found in logs (graceful termination)
Action     → Pod backend-5bf99597c-6nbfq restarted
Result     → Pod restarted successfully!
```

**Time to heal: < 30 seconds**

![Chaos Setup](docs/screenshots/21-chaos-setup.png)
![Pod Crash Detected](docs/screenshots/22-pod-crash-terminating.png)
![Full Demo — 3 Terminals](docs/screenshots/23-chaos-full-demo.png)
![Slack Incident Report](docs/screenshots/24-slack-chaos-notification.png)

---

## 🚀 Quick Start

### Prerequisites

```
- Python 3.10+
- Docker
- kubectl
- AWS CLI (configured with IAM user)
- Groq API key — free at console.groq.com
- Terraform 1.0+
```

### 1. Clone and Setup

```bash
git clone https://github.com/manesaurabh1704-devops/ai-autonomous-devops-healer.git
cd ai-autonomous-devops-healer

pip install -r requirements.txt
cp .env.example .env
# Edit .env — add GROQ_API_KEY and SLACK_WEBHOOK_URL
```

### 2. Deploy Infrastructure

```bash
cd terraform
terraform init
terraform apply
```

### 3. Deploy Application

```bash
kubectl apply -f k8s/app/
kubectl apply -f k8s/agent/
```

### 4. Run Agent Locally

```bash
uvicorn agent.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Test Self-Healing

```bash
# Crash a pod
kubectl delete pod -l app=backend

# Trigger agent
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "Backend pod crashed. Check, fix, and report to Slack."}'
```

---

## 🌐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes (dev) | Groq API key — console.groq.com |
| `SLACK_WEBHOOK_URL` | Yes | Slack Incoming Webhook URL |
| `AWS_REGION` | Yes | AWS region (ap-south-1) |
| `PROMETHEUS_URL` | No | Prometheus service URL |
| `ALERTMANAGER_URL` | No | Alertmanager service URL |
| `USE_BEDROCK` | No | Set `true` for AWS Bedrock LLM |
| `KUBECONFIG` | No | Path to kubeconfig |

---

## 👨‍💻 Author

**Saurabh Mane** — DevOps Engineer

- 🐙 GitHub: [@manesaurabh1704-devops](https://github.com/manesaurabh1704-devops)
- 🐳 DockerHub: [manesaurabh1704devops](https://hub.docker.com/u/manesaurabh1704devops)
