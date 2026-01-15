# FastAPI Task Management - DevOps Project

## Overview
A production-ready FastAPI application demonstrating DevOps best practices including CI/CD, containerization, Kubernetes deployment, observability, and security scanning.

## Features
- RESTful API for task management
- Prometheus metrics exposure
- Structured logging with trace IDs
- Docker containerization
- Kubernetes deployment with auto-scaling
- CI/CD pipeline with security scans
- Grafana dashboards for monitoring

## Prerequisites
- Docker Desktop with Kubernetes enabled
- Python 3.11+
- kubectl CLI
- Git

## Local Development

### Running with Python
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app:app --reload --port 8000

# Test the API
curl http://localhost:8000/health
```

### Running with Docker Compose
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Kubernetes Deployment

### Deploy to Local Cluster
```bash
# Apply all manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Deploy monitoring
kubectl apply -f k8s/prometheus/
kubectl apply -f k8s/grafana/

# Verify deployment
kubectl get pods -n fastapi-app
```

### Access Services
- **API**: http://localhost:30080
- **Prometheus**: http://localhost:30090
- **Grafana**: http://localhost:30030 (admin/admin123)

## API Endpoints

### Create Task
```bash
curl -X POST http://localhost:30080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description"}'
```

### Get All Tasks
```bash
curl http://localhost:30080/tasks
```

### Get Specific Task
```bash
curl http://localhost:30080/tasks/1
```

### Delete Task
```bash
curl -X DELETE http://localhost:30080/tasks/1
```

### Health Check
```bash
curl http://localhost:30080/health
```

### Metrics
```bash
curl http://localhost:30080/metrics
```

## Observability

### Metrics
- Request count by endpoint, method, and status
- Request duration histograms
- Available at `/metrics` endpoint

### Logs
- Structured JSON logging
- Request tracing with unique trace IDs
- Log levels: INFO, WARNING, ERROR

### Dashboards
Access Grafana at http://localhost:30030 to view:
- Request rate trends
- Response time percentiles
- Error rates
- Request distribution by status code

## Security

### SAST (Static Analysis)
```bash
pip install bandit
bandit -r app.py
```

### DAST (Dynamic Analysis)
Automatically run in CI/CD pipeline using OWASP ZAP

## CI/CD Pipeline

### Stages
1. **Test**: Run pytest test suite
2. **SAST**: Bandit security scan
3. **Build**: Docker image build and push
4. **DAST**: OWASP ZAP security scan

### Triggering
```bash
git push origin main
```

View pipeline status: GitHub Actions tab

## Architecture
### Complete DevOps Pipeline
```mermaid
flowchart TD

%% =======================
%% LAYER 1: SOURCE CODE
%% =======================
subgraph L1["🧩 CODE LAYER - Source Control"]
    direction TB
    G[📦 GitHub Repository]
    
    G --> A["app.py - FastAPI Application"]
    G --> B["Dockerfile - Container Definition"]
    G --> C["k8s/ - Kubernetes Manifests"]
    G --> D[".github/workflows - CI/CD Pipeline"]
end

%% =======================
%% TRANSITION
%% =======================
T1["git push / pull request"]

%% =======================
%% LAYER 2: CI/CD
%% =======================
subgraph L2["⚙️ CI/CD PIPELINE - GitHub Actions"]
    direction TB
    CI[GitHub Actions]
    
    CI --> TST["🧪 Tests - Pytest"]
    CI --> SAST["🔒 SAST - Bandit"]
    CI --> BUILD["🔨 Build - Docker Image"]
    CI --> DAST["🛡️ DAST - OWASP ZAP"]
end

%% =======================
%% TRANSITION
%% =======================
T2["docker push"]

%% =======================
%% LAYER 3: REGISTRY
%% =======================
subgraph L3["📦 CONTAINER REGISTRY"]
    direction TB
    R[Docker Hub]
    R --> IMG1["fastapi-devops:latest"]
    R --> IMG2["fastapi-devops:commit-sha"]
end

%% =======================
%% TRANSITION
%% =======================
T3["kubectl apply"]

%% =======================
%% LAYER 4: KUBERNETES
%% =======================
subgraph L4["☸️ KUBERNETES CLUSTER"]
    direction TB
    
    CFG["ConfigMap - Environment Config"]
    DEP["Deployment - Replicas: 2-5"]
    POD1["Pod 1 - FastAPI Container"]
    POD2["Pod 2 - FastAPI Container"]
    SVC["Service - NodePort: 30080"]
    HPA["HPA - Auto-scaling"]
    
    CFG --> DEP
    DEP --> POD1
    DEP --> POD2
    POD1 --> SVC
    POD2 --> SVC
    HPA -.->|scales| DEP
end

%% =======================
%% TRANSITION
%% =======================
T4["HTTP Requests"]

%% =======================
%% LAYER 5: OBSERVABILITY & ACCESS
%% =======================
subgraph L5["🌐 APPLICATION & MONITORING"]
    direction TB
    
    API["FastAPI Endpoints - /health /tasks /metrics"]
    
    OBS["📊 Observability - Metrics + Logs + Tracing"]
    
    U["👥 Users / Clients"]
    
    U --> API
    API -.->|emits| OBS
end

%% =======================
%% FLOW CONNECTIONS
%% =======================
L1 --> T1
T1 --> L2
L2 --> T2
T2 --> L3
L3 --> T3
T3 --> L4
L4 --> T4
T4 --> L5

%% =======================
%% STYLING
%% =======================
classDef layer fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
classDef component fill:#ffffff,stroke:#90caf9,stroke-width:2px
classDef transition fill:#fff3e0,stroke:#ff9800,stroke-width:2px,stroke-dasharray:5 5
classDef highlight fill:#c8e6c9,stroke:#388e3c,stroke-width:3px

class L1,L2,L3,L4,L5 layer
class G,A,B,C,D,CI,TST,SAST,BUILD,DAST,R,IMG1,IMG2,CFG,POD1,POD2,API,OBS,U component
class T1,T2,T3,T4 transition
class DEP,SVC,HPA highlight
```


## Technologies Used
- **Backend**: FastAPI, Pydantic, Uvicorn
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes
- **Observability**: Prometheus, Grafana
- **CI/CD**: GitHub Actions
- **Security**: Bandit (SAST), OWASP ZAP (DAST)
- **Monitoring**: prometheus-client



## Project Structure
```
.
├── app.py                      # Main application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Local development
├── .github/
│   └── workflows/
│       └── ci-cd.yaml         # CI/CD pipeline
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   ├── prometheus/
│   └── grafana/
└── tests/
    └── test_app.py            # Test suite
```

## Cleanup
```bash
# Delete Kubernetes resources
kubectl delete namespace fastapi-app

# Stop Docker Compose
docker-compose down -v
```

## Author
Ghada MHADHBI

