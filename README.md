# 🚀 Kazestack DevOps Project

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-Latest-2496ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.5+-844fba.svg?style=flat&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Production-ready Kubernetes Flask application with enterprise-grade DevOps infrastructure on Azure. This project demonstrates modern cloud-native development practices including containerization, orchestration, infrastructure-as-code, monitoring, and security hardening.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Deployment Guide](#deployment-guide)
- [Configuration](#configuration)
- [Monitoring & Observability](#monitoring--observability)
- [Security](#security)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project showcases a complete DevOps workflow for deploying a Flask-based microservice on Kubernetes with Azure cloud infrastructure. It includes:

- **Multi-environment deployment** (Local → Docker → Kubernetes → Azure)
- **Infrastructure-as-Code** using Terraform for Azure Kubernetes Service (AKS)
- **Cloud-native architecture** with Kubernetes best practices
- **Production-grade security** and compliance configurations
- **Comprehensive monitoring** with Prometheus and structured logging

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Azure Cloud                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Azure Kubernetes Service (AKS)          │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Ingress Controller (NGINX)                  │   │  │
│  │  │  ├─ TLS/SSL Termination (cert-manager)      │   │  │
│  │  │  └─ Rate Limiting & Routing                 │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                      ↓                               │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  K8s-App Deployment (3-10 replicas)         │   │  │
│  │  │  ├─ Health Checks (Liveness/Readiness)      │   │  │
│  │  │  ├─ Resource Limits & Requests              │   │  │
│  │  │  └─ Anti-affinity Pod Scheduling            │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                      ↓                               │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Horizontal Pod Autoscaling (HPA)           │   │  │
│  │  │  └─ Scales based on CPU/Memory metrics      │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  │                      ↓                               │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │  Prometheus Monitoring Stack                 │   │  │
│  │  │  └─ Metrics collection & alerting            │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Virtual Network (VNet) with Network Security        │  │
│  │  └─ Subnet isolation & NSG rules                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    Local Development                         │
│  ├─ Flask Application (app.py)                             │
│  ├─ Docker Multi-stage Build                              │
│  └─ docker-compose for local testing                       │
└──────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### 🔒 Production Ready

- **Multi-stage Docker builds** - Optimized image sizes with security scanning
- **Prometheus metrics** - Comprehensive application & infrastructure metrics
- **Health checks** - Liveness & readiness probes for reliable operations
- **Structured logging** - JSON-formatted logs for centralized aggregation
- **Security hardening** - Non-root users, minimal capabilities, immutable filesystems

### ⚡ High Availability

- **Horizontal Pod Autoscaling** - Auto-scales 3-10 replicas based on demand
- **Rolling updates** - Zero-downtime deployments with gradual replica replacement
- **Pod Disruption Budgets** - Maintains minimum availability during node drains
- **Anti-affinity scheduling** - Distributes pods across nodes for fault tolerance
- **Circuit breakers** - Prevents cascading failures

### 📊 Monitoring & Observability

- **Prometheus metrics** - Application performance & resource utilization
- **Structured JSON logging** - Easy parsing and centralized log aggregation
- **Request tracing** - Request duration tracking per endpoint
- **Error tracking** - Error rate monitoring and alerting
- **Dashboard ready** - Compatible with Grafana

### 🔐 Security

- **Non-root container execution** - Runs as unprivileged user (UID 1000)
- **Read-only root filesystem** - Prevents runtime modifications
- **Capability dropping** - Minimal Linux capabilities
- **RBAC (Role-Based Access Control)** - Kubernetes least-privilege access
- **Network policies** - Ingress/egress traffic restrictions
- **TLS/SSL encryption** - HTTPS with automatic certificate management via cert-manager

## 🛠️ Tech Stack

| Category                   | Technologies                           |
| -------------------------- | -------------------------------------- |
| **Application**            | Python 3.11, Flask 2.3, Gunicorn       |
| **Containerization**       | Docker, Multi-stage builds             |
| **Orchestration**          | Kubernetes 1.28+                       |
| **Cloud Provider**         | Microsoft Azure (AKS)                  |
| **Infrastructure-as-Code** | Terraform                              |
| **Monitoring**             | Prometheus, Structured Logging         |
| **Networking**             | Nginx Ingress, Cert-manager            |
| **CI/CD**                  | GitHub Actions (ready for integration) |
| **Observability**          | Prometheus metrics, JSON logs          |

## 📊 Features

✅ **Production Ready**

- Multi-stage Docker builds
- Prometheus metrics
- Health checks (liveness & readiness probes)
- Structured logging
- Security best practices (non-root user, restricted capabilities)

✅ **High Availability**

- Horizontal Pod Autoscaling (HPA)
- Rolling updates
- Pod disruption budgets
- Affinity rules (anti-affinity scheduling)

✅ **Monitoring & Logging**

- Prometheus metrics endpoint
- Structured JSON logging
- Request duration tracking
- Error rate monitoring

✅ **Security**

- Non-root container user
- Read-only root filesystem
- No privilege escalation
- Minimal capabilities
- RBAC configuration
- TLS/SSL ready with cert-manager

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Kubernetes cluster (minikube, EKS, or AKS)
- kubectl CLI
- Terraform (for Azure infrastructure)

### Local Development

```bash
# Clone repository
git clone https://github.com/ElvisKazerwa/kazestack-devops-project.git
cd kazestack-devops-project

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python kazestack-devops-project/k8s-app/app.py

# Visit http://localhost:5000
# Metrics available at http://localhost:5000/metrics
# Health check at http://localhost:5000/health
```

### Docker Build & Run

```bash
# Build image with multi-stage build
docker build -t k8s-app:v1.0 .

# Run container locally
docker run -p 5000:5000 k8s-app:v1.0

# Or use docker-compose
docker-compose up -d
```

### Kubernetes Deployment (Quick)

```bash
# Create production namespace
kubectl create namespace production

# Deploy all resources
kubectl apply -f kazestack-devops-project/k8s/ -n production

# Check deployment status
kubectl get pods -n production
kubectl get svc -n production
kubectl get hpa -n production

# View logs
kubectl logs -n production deployment/k8s-app

# Port forward for testing
kubectl port-forward -n production svc/k8s-app 5000:5000

# Visit http://localhost:5000
```

## 🔧 Deployment Guide

### Azure Deployment (Terraform)

```bash
cd kazestack-devops-project/terraform-azure

# Initialize Terraform
terraform init

# Review infrastructure plan
terraform plan

# Deploy infrastructure
terraform apply

# Get AKS credentials
az aks get-credentials --resource-group <rg-name> --name <cluster-name>

# Deploy application to AKS
kubectl apply -f ../k8s/ -n production
```

See [TERRAFORM.md](kazestack-devops-project/terraform-azure/README.md) for detailed infrastructure setup.

## ⚙️ Configuration

### Environment Variables

| Variable    | Default    | Description                                |
| ----------- | ---------- | ------------------------------------------ |
| `PORT`      | 5000       | Flask application port                     |
| `FLASK_ENV` | production | Flask environment (development/production) |
| `WORKERS`   | 4          | Gunicorn worker processes                  |
| `LOG_LEVEL` | INFO       | Application logging level                  |

### Kubernetes Resources

| Resource           | Description            | Configuration                            |
| ------------------ | ---------------------- | ---------------------------------------- |
| **Deployment**     | Flask app replicas     | 3-10 replicas with rolling updates       |
| **Service**        | Internal load balancer | ClusterIP on port 5000                   |
| **HPA**            | Auto-scaling           | Scales 3-10 replicas based on CPU/Memory |
| **Ingress**        | External access        | HTTPS with TLS (cert-manager)            |
| **ServiceAccount** | RBAC permissions       | Minimal required permissions             |
| **NetworkPolicy**  | Traffic control        | Ingress from Ingress controller only     |

## 📊 Monitoring & Observability

### Prometheus Metrics

The application exposes Prometheus metrics at `/metrics` endpoint.

**Key Metrics:**

- `app_requests_total` - Total HTTP requests by method and endpoint
- `app_request_duration_seconds` - Request latency histogram
- `app_errors_total` - Total errors by type
- `process_cpu_seconds_total` - Process CPU usage
- `process_resident_memory_bytes` - Memory usage

**Accessing Metrics:**

```bash
# Locally
curl http://localhost:5000/metrics

# In Kubernetes
kubectl port-forward -n production svc/k8s-app 5000:5000
curl http://localhost:5000/metrics
```

### Health Checks

- `/health` - Liveness probe
- `/ready` - Readiness probe

### Structured Logging

The application uses JSON-formatted structured logging for production environments:

```json
{
  "timestamp": "2024-04-22T10:30:45.123Z",
  "level": "INFO",
  "request_id": "abc123",
  "message": "Request processed",
  "duration_ms": 45,
  "status": 200
}
```

## 🔐 Security

### Security Best Practices Implemented

- **Non-root execution** - Container runs as UID 1000 (`appuser`)
- **Minimal base image** - `python:3.11-slim` reduces attack surface
- **Read-only filesystem** - Root filesystem set to read-only
- **No privilege escalation** - `securityContext.allowPrivilegeEscalation: false`
- **Dropped capabilities** - Unnecessary Linux capabilities removed
- **Resource limits** - Memory and CPU limits prevent resource exhaustion
- **RBAC** - Kubernetes RBAC with minimal permissions
- **Network policies** - Restricts traffic to authorized sources
- **TLS/SSL** - HTTPS with automatic certificate rotation

### Vulnerability Management

- Regular dependency scanning with Trivy
- Automated CVE alerts
- Multi-stage builds reduce production image size
- No development dependencies in production

### Compliance

- Kubernetes Pod Security Standards (restricted profile)
- CIS Kubernetes benchmarks aligned
- OWASP application security best practices

## 📁 Project Structure

```
kazestack-devops-project/
├── README.md                          # Project overview & getting started
├── DEPLOYMENT.md                      # Deployment procedures
├── ARCHITECTURE.md                    # System architecture & design
├── CONTRIBUTING.md                    # Contribution guidelines
├── LICENSE                            # MIT License
├── Dockerfile                         # Multi-stage production Docker build
├── docker-compose.yml                 # Local development setup
├── prometheus.yml                     # Prometheus scrape configuration
├── requirements.txt                   # Python dependencies
├── deploy.sh                          # Shell deployment script
├── deploy.ps1                         # PowerShell deployment script
│
├── kazestack-devops-project/
│   ├── k8s-app/
│   │   ├── app.py                    # Flask application with metrics
│   │   ├── Dockerfile                # Container definition
│   │   ├── requirements.txt           # Python dependencies
│   │   ├── deployment.yaml            # K8s deployment manifest
│   │   └── service.yaml               # K8s service manifest
│   │
│   ├── k8s/
│   │   ├── deployment.yaml            # Main deployment configuration
│   │   ├── service.yml                # Service definition
│   │   ├── hpa.yml                    # Horizontal Pod Autoscaling
│   │   ├── ingress.yml                # Ingress with TLS
│   │   └── serviceaccount.yml         # RBAC configuration
│   │
│   └── terraform-azure/
│       ├── main.tf                    # Primary infrastructure resources
│       ├── variables.tf               # Input variables
│       ├── outputs.tf                 # Output values
│       ├── versions.tf                # Provider versions
│       ├── locals.tf                  # Local values
│       ├── terraform.tfvars.example   # Example variables file
│       └── README.md                  # Terraform documentation
```

## 🔄 CI/CD Integration

### GitHub Actions

This project is ready for GitHub Actions CI/CD pipeline:

1. **Build** - Multi-stage Docker build with layer caching
2. **Test** - Unit tests and integration tests
3. **Security Scan** - Trivy vulnerability scanning
4. **Deploy** - Automated deployment to Kubernetes

Example workflow would include:

- Build and push to Docker registry
- Run security scans
- Deploy to staging cluster
- Run smoke tests
- Deploy to production with blue-green strategy

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code style guidelines
- Pull request process
- Development setup
- Testing requirements
- Commit message conventions

### Development Setup

```bash
# Clone repository
git clone https://github.com/ElvisKazerwa/kazestack-devops-project.git
cd kazestack-devops-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 kazestack-devops-project/
pylint kazestack-devops-project/

# Format code
black kazestack-devops-project/
```

## 📚 Documentation

- **[README.md](README.md)** - Project overview and quick start
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Detailed deployment procedures
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design decisions
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[Terraform README](kazestack-devops-project/terraform-azure/README.md)** - Infrastructure setup

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Elvis Kazerwa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

**Elvis Kazerwa**

- GitHub: [@ElvisKazerwa](https://github.com/ElvisKazerwa)
- LinkedIn: [Your LinkedIn Profile]

## 🙏 Acknowledgments

- Flask and Gunicorn teams for excellent Python web frameworks
- Kubernetes community for container orchestration standards
- Terraform team for infrastructure-as-code tools
- Azure community for cloud platform support

## 📞 Support & Questions

For questions, issues, or suggestions:

1. Open an issue on [GitHub Issues](https://github.com/ElvisKazerwa/kazestack-devops-project/issues)
2. Start a discussion on [GitHub Discussions](https://github.com/ElvisKazerwa/kazestack-devops-project/discussions)
3. Check existing documentation and troubleshooting guides

### Required Secrets

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub token
- `KUBE_CONFIG` - Kubernetes config (base64 encoded)

## Production Checklist

- [ ] Update Docker Hub credentials in GitHub Secrets
- [ ] Update Kubernetes credentials in GitHub Secrets
- [ ] Update domain in Ingress (kazestack.com)
- [ ] Install cert-manager in cluster
- [ ] Install nginx-ingress controller
- [ ] Configure metrics server for HPA
- [ ] Set up Prometheus for monitoring
- [ ] Enable pod security policies
- [ ] Configure network policies
- [ ] Set up alerting rules

## Troubleshooting

### Pod not starting

```bash
kubectl describe pod <pod-name> -n production
kubectl logs <pod-name> -n production
```

### Metrics not working

```bash
curl http://localhost:5000/metrics
```

### HPA not scaling

```bash
kubectl get hpa -n production
kubectl describe hpa k8s-app-hpa -n production
```
