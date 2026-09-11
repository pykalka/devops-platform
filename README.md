# DevOps Platform

[![CI/CD](https://github.com/pykalka/devops-platform/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/pykalka/devops-platform/actions/workflows/ci-cd.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5)](https://kubernetes.io/)

A small Python REST API deployed to Kubernetes with an automated CI/CD pipeline, PostgreSQL persistence, monitoring, and centralized logging.

The project demonstrates a complete application delivery workflow:

Git → CI tests → Docker build → Container Registry → Kubernetes → Monitoring & Logging
## Project Overview

DevOps Platform is a task management REST API built with FastAPI and PostgreSQL.

The main goal of the project is to demonstrate practical DevOps practices around:

application containerization;
automated testing;
CI/CD automation;
Docker image versioning;
Kubernetes deployment;
database persistence;
health checks;
resource management;
metrics collection;
monitoring dashboards;
centralized container logging.

The project is designed as a local Kubernetes environment using Minikube.

## Architecture
                         ┌─────────────────┐
                         │     GitHub      │
                         └────────┬────────┘
                                  │ git push
                                  ▼
                         ┌─────────────────┐
                         │ GitHub Actions  │
                         │                 │
                         │  pytest        │
                         │  Docker build  │
                         │  Docker push   │
                         │  K8s deploy    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │      GHCR       │
                         │ Docker Registry │
                         └────────┬────────┘
                                  │
                                  ▼
                  ┌────────────────────────────┐
                  │        Kubernetes         │
                  │       devops-platform     │
                  │                            │
                  │  ┌──────────────────────┐  │
                  │  │    FastAPI Backend   │  │
                  │  └──────────┬───────────┘  │
                  │             │              │
                  │  ┌──────────▼───────────┐  │
                  │  │     PostgreSQL       │  │
                  │  │        + PVC         │  │
                  │  └──────────────────────┘  │
                  └─────────────┬──────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
             ┌──────────────┐        ┌──────────────┐
             │  Prometheus  │        │   Promtail   │
             └──────┬───────┘        └──────┬───────┘
                    │                       │
                    ▼                       ▼
             ┌──────────────┐        ┌──────────────┐
             │   Grafana    │        │     Loki     │
             └──────────────┘        └──────────────┘
## Tech Stack

### Application
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest

### Containerization
- Docker
- Docker Compose
- GitHub Container Registry (GHCR)

### CI/CD
- GitHub Actions
- Self-hosted GitHub Actions runner
- Immutable Docker image tags based on Git commit SHA

### Kubernetes
- Kubernetes
- Minikube
- kubectl
- Helm
- ConfigMap
- Secret
- PersistentVolumeClaim
- Services
- RollingUpdate
- Readiness and liveness probes
- Resource requests and limits

### Monitoring and Logging
- Prometheus
- Grafana
- Loki
- Promtail
- Prometheus FastAPI Instrumentator

## Project Structure
devops-platform/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── conftest.py
│   └── test_api.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.example.yaml
│   ├── postgres.yaml
│   ├── postgres-service.yaml
│   ├── backend.yaml
│   ├── backend-service.yaml
│   ├── prometheus.yaml
│   └── grafana.yaml
│
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── loki/
│   │   └── values.yaml
│   └── promtail/
│       └── values.yaml
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
└── README.md
## Application API

The application provides the following endpoints:

Method	Endpoint	Description
GET	/health	Health check
POST	/tasks	Create a task
GET	/tasks	Get all tasks
GET	/tasks/{task_id}	Get a task
PUT	/tasks/{task_id}	Update a task
DELETE	/tasks/{task_id}	Delete a task
GET	/metrics	Prometheus metrics

FastAPI also provides interactive API documentation:

```text
/docs
/redoc
```
Example

Create a task:


```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Kubernetes",
    "description": "Deploy the application to Minikube"
  }'
```

Get all tasks:


```bash
curl http://localhost:8000/tasks
```

Health check:


```bash
curl http://localhost:8000/health
```

Expected response:

{
  "status": "ok"
}
## Local Development
1. Clone the repository
git clone git@github.com:pykalka/devops-platform.git
cd devops-platform
2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a local .env file based on .env.example:

cp .env.example .env

Edit .env and set the required database credentials.

5. Start PostgreSQL

PostgreSQL can be started using Docker Compose:

docker compose up -d postgres
6. Run database migrations
alembic upgrade head
7. Start the application
uvicorn app.main:app --reload

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```
## Docker Compose

The project includes a Docker Compose configuration for local containerized development.

Start the complete application stack:


```bash
docker compose up -d --build
```

Check running containers:


```bash
docker compose ps
```

View application logs:


```bash
docker compose logs -f backend
```

Stop the stack:


```bash
docker compose down
```

PostgreSQL data is stored in a named Docker volume:

postgres_data
## Database Migrations

Alembic is used to manage database schema migrations.

Apply migrations:


```bash
alembic upgrade head
```

Create a new migration:


```bash
alembic revision --autogenerate -m "describe change"
```

The Docker container automatically applies migrations before starting the application.

This behavior is implemented in entrypoint.sh.

## Kubernetes Deployment

The application is deployed to a local Kubernetes cluster running on Minikube.

1. Start Minikube
minikube start

Check the cluster:

kubectl get nodes
2. Create the namespace
kubectl apply -f k8s/namespace.yaml
3. Create the Kubernetes Secret

The real secret file is intentionally not stored in Git.

Create it from the example:

cp k8s/secret.example.yaml k8s/secret.yaml

Edit k8s/secret.yaml and replace the example credentials.

Then apply it:

kubectl apply -f k8s/secret.yaml
4. Apply the remaining manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/backend.yaml

Check the deployed resources:


```bash
kubectl get pods -n devops-platform
kubectl get services -n devops-platform
kubectl get deployments -n devops-platform
```

Check the backend rollout:

kubectl rollout status deployment/backend -n devops-platform
## Kubernetes Resources

The Kubernetes configuration includes:

Namespace for application isolation;
ConfigMap for non-sensitive configuration;
Secret for database credentials;
Deployment for the backend;
Deployment and PVC for PostgreSQL;
Service objects for internal communication;
readiness and liveness probes;
CPU and memory requests/limits;
rolling update strategy.

The backend uses an immutable image tag based on the Git commit SHA.

For example:


```text
ghcr.io/pykalka/devops-platform:<commit-sha>
```

This allows every Kubernetes deployment to reference a specific version of the application.

## Configuration and Secrets

Sensitive values are not committed to the repository.

The following local files are ignored by Git:


```text
.env
k8s/secret.yaml
```

Example configuration files are provided:


```text
.env.example
k8s/secret.example.yaml
```

Before deploying the application manually, create the real files from their examples and configure the required credentials.

## CI/CD

The CI/CD pipeline is implemented with GitHub Actions.

The workflow is triggered by pushes and pull requests to the master branch.

Pipeline
Git Push
   │
   ▼
Run Pytest
   │
   ▼
Build Docker Image
   │
   ▼
Push Image to GHCR
   │
   ▼
Deploy to Kubernetes
   │
   ▼
Wait for Rollout
   │
   ▼
Check Pods and Services
Test stage

The CI pipeline starts a PostgreSQL service and runs the automated test suite.

python -m pytest
Build stage

After successful tests, GitHub Actions builds the Docker image.

The image is tagged with the Git commit SHA:

ghcr.io/pykalka/devops-platform:<commit-sha>

The latest tag is also published for convenience.

Deployment stage

The deployment job runs on a self-hosted GitHub Actions runner with access to the local Kubernetes cluster.

Before applying the manifests, the workflow replaces:


```text
IMAGE_TAG
```

in the Kubernetes backend manifest with the current Git commit SHA.

This makes each deployment use a unique immutable image version and ensures that a new Kubernetes rollout is triggered for every new commit.

## Monitoring

The project uses Prometheus and Grafana for application monitoring.

FastAPI exposes metrics through:


```text
/metrics
```

Prometheus periodically scrapes the backend metrics endpoint.

The main metrics include HTTP request counters and request status information.

Grafana Dashboard

The Grafana dashboard contains panels for:

HTTP request rate;
total HTTP requests;
requests grouped by endpoint;
HTTP error rate.

Example PromQL query:


```promql
rate(http_requests_total{job="devops-platform-backend"}[1m])
```

Prometheus and Grafana are deployed inside the Kubernetes environment.

Grafana can be accessed locally using port forwarding:


```bash
kubectl port-forward svc/grafana 3000:3000 -n devops-platform
```

Then open:

```text
http://localhost:3000
```
## Centralized Logging

The project uses Loki and Promtail for centralized container logging.

The logging flow is:


```text
Kubernetes Pods
      │
      ▼
   Promtail
      │
      ▼
     Loki
      │
      ▼
    Grafana
```

Promtail discovers Kubernetes pods and forwards container logs to Loki.

Logs can then be queried in Grafana using LogQL.

Example query:

{namespace="devops-platform", pod=~"backend-.*"}
Note about Promtail

Promtail is used in this project to demonstrate Kubernetes log collection and the Loki logging pipeline.

Promtail has reached End-of-Life. A production-oriented implementation should migrate to Grafana Alloy.

## Health Checks

The backend exposes:


```text
GET /health
```

Kubernetes uses this endpoint for:

readiness probes;
liveness probes.

Readiness probes prevent traffic from being sent to a pod that is not ready.

Liveness probes allow Kubernetes to restart a container when the application becomes unhealthy.

## Resource Management

The backend Kubernetes Deployment defines CPU and memory requests and limits.

Example:


```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

This demonstrates basic Kubernetes resource management and prevents the application from consuming unlimited cluster resources.

## Testing

The project contains an automated API test suite using Pytest.

Run tests locally:


```bash
python -m pytest
```

The test environment uses a separate PostgreSQL database.

The CI pipeline also runs the tests before building and publishing the Docker image.

## Future Improvements

Possible improvements include:

migration from Promtail to Grafana Alloy;
deployment to a cloud Kubernetes cluster;
HTTPS/TLS configuration;
Kubernetes Ingress;
Helm chart for the application;
PostgreSQL high availability;
persistent monitoring storage;
more detailed application metrics;
alerting with Alertmanager;
secrets management using a dedicated secret-management solution;
infrastructure provisioning with Terraform.
## Purpose

This project was created as a practical DevOps portfolio project to demonstrate an end-to-end workflow for developing, testing, containerizing, deploying, monitoring, and logging a Python application.

The focus is on understanding how the individual tools work together as one delivery pipeline rather than using them as isolated technologies.
