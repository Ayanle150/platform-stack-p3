# Platform Stack P3

A production-grade platform engineering stack built on Azure, demonstrating modern DevOps practices end-to-end.

## Architecture

```
GitHub (source code)
    │  push to main
    ▼
GitHub Actions CI/CD
    ├── Build Docker images
    ├── Push to Azure Container Registry
    └── Deploy to AKS with Helm
            │
            ▼
    Azure Kubernetes Service
        ├── api pods (2–10, autoscaling)
        └── frontend pods (2–10, autoscaling)

Supporting services:
    ├── Azure Container Registry  — image storage
    ├── Azure Key Vault           — encrypted secrets
    └── Azure Monitor             — logging and alerting
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Application | Python, FastAPI, Uvicorn |
| Containerization | Docker (multi-stage builds) |
| Orchestration | Kubernetes (AKS) |
| Infrastructure | Terraform |
| Packaging | Helm |
| CI/CD | GitHub Actions + OIDC |
| Secrets | Azure Key Vault |
| Monitoring | Azure Monitor, Container Insights |

## Services

**`api`** — REST API serving JSON data on port 8000. Endpoints: `GET /`, `GET /health`, `GET /ready`, `GET /api/items`, `GET /api/items/{id}`

**`frontend`** — HTML frontend on port 8001. Fetches data from api and renders it as a webpage.

## Project Structure

```
platform-stack-p3/
├── services/
│   ├── api/                  # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── routers/
│   │   │       ├── health.py
│   │   │       └── items.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── frontend/             # FastAPI frontend
│       ├── app/
│       │   ├── main.py
│       │   └── routers/
│       │       ├── health.py
│       │       └── pages.py
│       ├── Dockerfile
│       └── requirements.txt
├── terraform/                # Azure infrastructure
│   ├── versions.tf
│   ├── variables.tf
│   ├── main.tf
│   └── outputs.tf
├── helm/                     # Kubernetes packaging
│   ├── api/
│   └── frontend/
├── .github/workflows/        # CI/CD pipelines
│   ├── ci.yml               # Build and push images
│   └── cd.yml               # Deploy to AKS
└── docker-compose.yml        # Local development
```

## Local Development

**Prerequisites:** Docker, Python 3.12+

```bash
# Run both services locally
docker compose up --build

# api:      http://localhost:8000
# frontend: http://localhost:8001
```

Run without Docker:
```bash
cd services/api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Infrastructure

**Prerequisites:** Azure CLI, Terraform >= 1.7, an Azure subscription

Before running Terraform, create the remote state backend manually (one-time):

```bash
az login
az group create --name rg-platform-state --location norwayeast
az storage account create --name <unique-name> --resource-group rg-platform-state \
  --location norwayeast --sku Standard_LRS
az storage container create --name tfstate --account-name <unique-name>
```

Update `terraform/versions.tf` with your storage account name, then:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

This provisions: Resource Group, AKS cluster, Azure Container Registry, Azure Key Vault, and all necessary role assignments.

## CI/CD Setup

Authentication uses OIDC — no stored credentials.

1. Create an App Registration in Azure:
```bash
az ad app create --display-name "github-<your-repo>"
az ad sp create --id <app-id>
az ad app federated-credential create --id <app-id> --parameters '{
  "name": "github-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:<owner>/<repo>:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'
az role assignment create --assignee <app-id> --role Contributor \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-platform-p3-dev
az role assignment create --assignee <app-id> --role AcrPush \
  --scope /subscriptions/<sub-id>/resourceGroups/rg-platform-p3-dev/providers/Microsoft.ContainerRegistry/registries/<acr-name>
```

2. Add these secrets to your GitHub repository (Settings → Secrets → Actions):

| Secret | Value |
|--------|-------|
| `AZURE_CLIENT_ID` | App Registration client ID |
| `AZURE_TENANT_ID` | Azure tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID |
| `ACR_NAME` | Container registry name |
| `RESOURCE_GROUP` | `rg-platform-p3-dev` |
| `AKS_CLUSTER_NAME` | AKS cluster name |

Push to `main` to trigger the pipeline.

## Kubernetes

Connect to the cluster:
```bash
az aks get-credentials --resource-group rg-platform-p3-dev --name aks-platform-p3-dev
```

Useful commands:
```bash
kubectl get pods                        # running pods
kubectl get services                    # services and IPs
kubectl logs -f <pod-name>              # live logs
kubectl describe pod <pod-name>         # troubleshoot a pod
kubectl get events --sort-by=.lastTimestamp  # recent events
```

Deploy manually with Helm:
```bash
helm upgrade --install api ./helm/api \
  --set image.repository=<acr>.azurecr.io/api \
  --set image.tag=<git-sha> \
  --set service.type=LoadBalancer

helm upgrade --install frontend ./helm/frontend \
  --set image.repository=<acr>.azurecr.io/frontend \
  --set image.tag=<git-sha> \
  --set service.type=LoadBalancer \
  --set env.API_URL=http://<api-ip>:8000
```

## Monitoring

After deployment, enable Container Insights:
```bash
az monitor log-analytics workspace create \
  --resource-group rg-platform-p3-dev \
  --workspace-name log-platform-p3-dev \
  --location norwayeast

az aks enable-addons \
  --resource-group rg-platform-p3-dev \
  --name aks-platform-p3-dev \
  --addons monitoring \
  --workspace-resource-id <workspace-resource-id>
```

View logs in Azure Portal → Log Analytics → Logs:
```kusto
ContainerLog
| where TimeGenerated > ago(1h)
| where ContainerName contains "api"
| order by TimeGenerated desc
```

---

Built as a complete platform engineering reference — from local development to production on Azure.
