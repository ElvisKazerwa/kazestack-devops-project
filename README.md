# K8s Production App

Production-ready Kubernetes Flask application with comprehensive DevOps setup.

## Features

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

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python k8s-app/app.py

# Visit http://localhost:5000
```

### Docker Build

```bash
# Build image
docker build -t k8s-app:v1.0 .

# Run container
docker run -p 5000:5000 k8s-app:v1.0
```

### Kubernetes Deployment

```bash
# Create production namespace
kubectl create namespace production

# Deploy application
kubectl apply -f k8s/

# Check status
kubectl get pods -n production
kubectl logs -n production deployment/k8s-app

# Port forward for testing
kubectl port-forward -n production svc/k8s-app 8080:80
```

## Configuration

### Environment Variables

- `PORT` - Server port (default: 5000)
- `FLASK_ENV` - Flask environment (development/production)

### Kubernetes Resources

- **Deployment** - 3 replicas with rolling updates
- **Service** - ClusterIP service
- **HPA** - Auto-scales 3-10 replicas based on CPU/Memory
- **Ingress** - HTTPS with cert-manager
- **ServiceAccount** - RBAC with minimal permissions

## Monitoring

### Prometheus Metrics

Endpoint: `/metrics`

Key metrics:
- `app_requests_total` - Total requests by method/endpoint
- `app_request_duration_seconds` - Request latency

### Health Checks

- `/health` - Liveness probe
- `/ready` - Readiness probe

## CI/CD Pipeline

GitHub Actions workflow:
1. Build - Multi-stage Docker build with caching
2. Security Scan - Trivy vulnerability scanning
3. Deploy - Blue-green deployment to Kubernetes

### Required Secrets

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub token
- `KUBE_CONFIG` - Kubernetes config (base64 encoded)

## Production Checklist

- [ ] Update Docker Hub credentials in GitHub Secrets
- [ ] Update Kubernetes credentials in GitHub Secrets
- [ ] Update domain in Ingress (k8s-app.example.com)
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
