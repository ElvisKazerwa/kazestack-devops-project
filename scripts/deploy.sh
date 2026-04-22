#!/bin/bash
# Deployment script for Linux/Mac
# Usage: ./deploy.sh [env] [region]

set -e

ENVIRONMENT=${1:-dev}
REGION=${2:-eastus}
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$SCRIPT_DIR/.."

echo "========================================="
echo "Deploying to $ENVIRONMENT environment"
echo "Region: $REGION"
echo "========================================="

# Deploy Terraform
echo ""
echo "[1/2] Applying Terraform configuration..."
cd "$REPO_ROOT/infra/terraform/envs/$ENVIRONMENT"
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# Deploy Kubernetes
echo ""
echo "[2/2] Deploying Kubernetes manifests..."
cd "$REPO_ROOT"
kubectl apply -k "infra/k8s/overlays/$ENVIRONMENT/"

echo ""
echo "========================================="
echo "Deployment completed successfully!"
echo "========================================="
