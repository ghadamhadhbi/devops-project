# 🛠️ DevOps Project – Task Management API

## 📌 Project Overview

This project is a complete **end-to-end DevOps implementation** of a lightweight backend REST API built with **FastAPI**.  
The goal is to apply modern DevOps practices from development to **CI/CD automation, containerization, observability, security, and Kubernetes deployment**.

The application provides a simple **Task Management API**.

---

## 🎯 Project Objectives

- Build a small backend REST API (<150 lines of code)
- Use Git & GitHub with issues, pull requests, and reviews
- Implement CI/CD using GitHub Actions
- Add observability (metrics, logs, tracing)
- Perform security scans (SAST + DAST)
- Containerize using Docker & Docker Compose
- Deploy on Kubernetes (Minikube/Kind)
- Document the project and present results



## 🧪 Backend Service

### Technology
- **FastAPI** (Python)
- **Pydantic** for data validation
- **Prometheus client** for metrics

### API Endpoints

| Method | Endpoint      | Description        |
|--------|---------------|--------------------|
| GET    | `/`           | API information    |
| GET    | `/health`     | Health check       |
| GET    | `/tasks`      | List all tasks     |
| POST   | `/tasks`      | Create a task      |
| GET    | `/tasks/{id}` | Get task by ID     |
| DELETE | `/tasks/{id}` | Delete task        |
| GET    | `/metrics`    | Prometheus metrics |

---

## 📊 Observability

### Metrics
Exposed via `/metrics` (Prometheus format):
- HTTP request count
- Request duration
- Requests per endpoint

### Logs
- Structured logging with Python `logging`
- Includes method, endpoint, status code, duration, and `trace_id`

### Tracing
Lightweight request tracing using a unique UUID per request (log correlation).

---

## 🔐 Security

### SAST – Static Application Security Testing
- Tool: **Bandit**
- Runs in CI; reports uploaded as artifacts

### DAST – Dynamic Application Security Testing
- Tool: **OWASP ZAP Baseline**
- Scans the running Docker container
- Reports in HTML & JSON

---

## 🐳 Containerization

### Docker
- Base image: `python:3.11-slim`
- Runs as non-root user
- Built-in health check

### Docker Compose (local development)
```bash
docker compose up --build
```
Application available at: **http://localhost:8000**

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

### Stages
1. **Tests** – Pytest + test report
2. **Security – SAST** – Bandit
3. **Build & Push** – Docker image → Docker Hub
4. **Security – DAST** – OWASP ZAP

**Triggers**: `push` to `main` and pull requests.

---

## ☸️ Kubernetes Deployment

### Resources
- Namespace
- Deployment (replicas, rolling updates)
- Service (NodePort)
- ConfigMap
- Startup/readiness/liveness probes
- Horizontal Pod Autoscaler (HPA – CPU & memory)

### Apply
```bash
kubectl apply -f k8s/
```

### Access
```bash
minikube service fastapi-service -n fastapi-app
```

---

## 📈 Monitoring Stack (Prometheus + Grafana)

- **Prometheus** scrapes `/metrics` (namespace: `monitoring`)
- **Grafana** dashboards show request rate, latency, and per-endpoint metrics

### Access Grafana
```bash
minikube service grafana -n monitoring
```
Default credentials: `admin` / `admin`

---

## 📁 Repository Structure

```
.
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── hpa.yaml
├── .github/workflows/
│   └── ci-cd.yml
└── README.md
```

---

## 📦 Docker Image

Published on Docker Hub:  
**`ghadamh/fastapi-devops:latest`**

---

## 📘 Lessons Learned

- Importance of health checks and probes in Kubernetes
- Difference between liveness and readiness probes
- CI/CD pipelines improve reliability and security
- Observability is essential for production systems
- Kubernetes enables scalability and resilience

---

## 🎓 Conclusion

This project demonstrates core DevOps principles including automation, security, monitoring, and container orchestration in a realistic yet educational pipeline.

---

## 🙌 Author

**Ghada Mhadhbi**  
DevOps & Software Engineering Student
