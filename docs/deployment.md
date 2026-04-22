# Deployment Guide

## Prerequisites

- Azure CLI installed and authenticated
- Terraform >= 1.0
- kubectl configured for your AKS cluster
- Docker (for building images)

## Deployment Steps

### Development Environment

```bash
cd infra/terraform/envs/dev
terraform init
terraform plan
terraform apply
```

### Production Environment

```bash
cd infra/terraform/envs/prod
terraform init
terraform plan
terraform apply
```

## Applying Kubernetes Manifests

```bash
kubectl apply -k infra/k8s/overlays/dev/    # for dev
kubectl apply -k infra/k8s/overlays/prod/   # for prod
```

## Rollback Procedures

To rollback a failed deployment:

```bash
kubectl rollout undo deployment/kazestack-devops-project -n default
```
