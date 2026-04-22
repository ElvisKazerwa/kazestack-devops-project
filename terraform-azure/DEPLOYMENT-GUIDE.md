# Terraform Azure Deployment Guide

This guide provides comprehensive instructions for deploying the Kazestack DevOps project infrastructure on Microsoft Azure using Terraform.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Post-Deployment](#post-deployment)
- [Management](#management)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)

## Overview

This Terraform configuration deploys a production-ready Azure Kubernetes Service (AKS) cluster with:

- **Virtual Network** - Isolated network with configurable subnets
- **Network Security Group** - Firewall rules for traffic control
- **Azure Kubernetes Service** - Managed Kubernetes cluster
- **Container Registry** - Private Docker image repository
- **Resource Group** - Logical container for resources

### Architecture

```
Azure Subscription
├── Resource Group
│   ├── Virtual Network (VNet)
│   │   ├── AKS Subnet (10.0.1.0/24)
│   │   └── Network Security Group
│   ├── AKS Cluster
│   │   ├── Node Pools
│   │   ├── System Pods
│   │   └── Ingress Controller
│   └── Container Registry (ACR)
```

## Prerequisites

### Local Machine Setup

#### 1. Install Required Tools

**Azure CLI**

```bash
# macOS
brew install azure-cli

# Linux (Ubuntu/Debian)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows (PowerShell)
# Download from: https://aka.ms/installazurecliwindows
```

**Terraform**

```bash
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
unzip terraform_1.5.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Windows
choco install terraform
```

**kubectl**

```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Windows (PowerShell)
choco install kubernetes-cli
```

**Verify Installation**

```bash
az --version
terraform version
kubectl version --client
```

#### 2. Azure Account Setup

```bash
# Login to Azure
az login

# List available subscriptions
az account list --output table

# Set default subscription
az account set --subscription <subscription-id>

# Verify login
az account show
```

### Azure Permissions

Your Azure account needs these permissions:

- Subscription: Owner or Contributor role
- Or custom role with permissions for:
  - Microsoft.Compute/\*
  - Microsoft.Network/\*
  - Microsoft.ContainerService/\*
  - Microsoft.ContainerRegistry/\*
  - Microsoft.Resources/\*

## Project Structure

```
terraform-azure/
├── main.tf                    # Primary resource definitions
├── variables.tf               # Input variables and defaults
├── outputs.tf                 # Output values
├── locals.tf                  # Local values and computed values
├── versions.tf                # Provider versions
├── terraform.tfvars           # Environment-specific values (DO NOT commit!)
├── terraform.tfvars.example   # Example file (commit this)
└── README.md                  # Terraform documentation

Key Files:
main.tf          - Defines all Azure resources (VNet, AKS, ACR, NSG, etc.)
variables.tf     - Input variables with descriptions and defaults
outputs.tf       - Outputs for cluster endpoint, kubeconfig, etc.
locals.tf        - Local values and computed variables
versions.tf      - Provider configuration and version constraints
```

## Configuration

### Step 1: Prepare Variables File

```bash
# Navigate to terraform directory
cd kazestack-devops-project/terraform-azure

# Copy example file
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
nano terraform.tfvars  # or use your preferred editor
```

### Step 2: Configure terraform.tfvars

```hcl
# terraform.tfvars

# Azure region for deployment
location = "eastus"

# Resource naming
resource_group_name = "kazestack-rg"
cluster_name        = "kazestack-cluster"

# Network configuration
vnet_address_space = ["10.0.0.0/16"]
subnet_address_prefixes = {
  aks = ["10.0.1.0/24"]
}

# AKS Configuration
node_count      = 3
vm_size         = "Standard_D2s_v3"
max_pods        = 30
os_disk_size_gb = 50

# Kubernetes version (must be supported by Azure)
kubernetes_version = "1.27"

# Tags for resource organization
environment = "production"
project     = "kazestack"
managed_by  = "terraform"
```

### Variable Reference

| Variable                  | Type   | Default                  | Description         |
| ------------------------- | ------ | ------------------------ | ------------------- |
| `location`                | string | "eastus"                 | Azure region        |
| `resource_group_name`     | string | "kazestack-rg"           | Resource group name |
| `cluster_name`            | string | "kazestack-cluster"      | AKS cluster name    |
| `vnet_address_space`      | list   | ["10.0.0.0/16"]          | VNet address range  |
| `subnet_address_prefixes` | map    | {"aks": ["10.0.1.0/24"]} | Subnet ranges       |
| `node_count`              | number | 3                        | Initial node count  |
| `vm_size`                 | string | "Standard_D2s_v3"        | VM size for nodes   |
| `max_pods`                | number | 30                       | Max pods per node   |
| `kubernetes_version`      | string | "1.27"                   | K8s version         |

### Supported VM Sizes

```
# Development
Standard_B2s    - 2 vCPU, 4 GB RAM (low cost)
Standard_B2ms   - 2 vCPU, 8 GB RAM

# Production
Standard_D2s_v3 - 2 vCPU, 8 GB RAM (recommended)
Standard_D4s_v3 - 4 vCPU, 16 GB RAM
Standard_D8s_v3 - 8 vCPU, 32 GB RAM
```

## Deployment

### Step 1: Initialize Terraform

```bash
# Navigate to terraform directory
cd kazestack-devops-project/terraform-azure

# Initialize working directory
terraform init

# Expected output:
# - Backend initialized
# - Modules loaded
# - Providers installed
```

### Step 2: Validate Configuration

```bash
# Validate Terraform files
terraform validate

# Expected output:
# Success! The configuration is valid.
```

### Step 3: Review Infrastructure Plan

```bash
# Generate execution plan
terraform plan -out=tfplan

# Review the plan (this shows what will be created)
# Expected: +N resources to add, 0 to change, 0 to destroy

# Save plan to file for later review
terraform plan -out=tfplan
```

### Step 4: Apply Configuration

```bash
# Apply the infrastructure
terraform apply tfplan

# Or apply without saved plan (will show plan first):
terraform apply

# When prompted, type "yes" to confirm
# Expected duration: 10-15 minutes

# Outputs will show:
# - Resource Group ID
# - AKS Cluster Endpoint
# - Kubeconfig download command
```

### Step 5: Retrieve Kubeconfig

```bash
# Get AKS credentials
az aks get-credentials \
  --resource-group $(terraform output -raw resource_group_name) \
  --name $(terraform output -raw aks_cluster_name)

# Verify connectivity
kubectl cluster-info
kubectl get nodes

# Expected: Nodes in "Ready" status
```

## Post-Deployment

### Step 1: Install Required Components

**Metrics Server (for HPA)**

```bash
# Install metrics-server for Horizontal Pod Autoscaling
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify
kubectl get deployment metrics-server -n kube-system
```

**NGINX Ingress Controller**

```bash
# Add Helm repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX ingress
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer

# Get external IP
kubectl get svc -n ingress-nginx

# Expected: External IP assigned to ingress-nginx-controller
```

**Cert-Manager (for TLS Certificates)**

```bash
# Add Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true

# Verify
kubectl get crds | grep cert-manager
```

### Step 2: Deploy Application

```bash
# Create namespace
kubectl create namespace production

# Deploy application resources
kubectl apply -f ../../kazestack-devops-project/k8s/ -n production

# Verify deployment
kubectl get all -n production
kubectl get hpa -n production

# Check logs
kubectl logs -n production deployment/kazestack
```

### Step 3: Configure Ingress (Optional)

```bash
# Get Ingress IP
kubectl get ingress -n production

# Update DNS records to point to ingress IP
# Or use dynamic DNS for testing

# Test access
curl http://<ingress-ip>/
curl http://<ingress-ip>/health
```

## Management

### View Outputs

```bash
# Display all outputs
terraform output

# Display specific output
terraform output -raw aks_cluster_endpoint
terraform output -raw kubeconfig_path

# Example outputs:
# aks_cluster_endpoint = "kazestack-cluster.eastus.azmk8s.io"
# resource_group_id = "/subscriptions/.../resourceGroups/kazestack-rg"
```

### Update Configuration

```bash
# Modify terraform.tfvars
nano terraform.tfvars

# Plan changes
terraform plan

# Apply changes
terraform apply

# Example: Scale node count
# node_count = 3 → 5
# terraform apply
```

### Destroy Infrastructure

```bash
# Review what will be destroyed
terraform plan -destroy

# Destroy all resources
terraform destroy

# When prompted, type "yes" to confirm
# Warning: This deletes all resources including data!
```

### Backup Terraform State

```bash
# State file contains infrastructure configuration
# NEVER commit state file to Git!

# Backup state
cp terraform.tfstate terraform.tfstate.backup

# View state (sensitive information!)
terraform show

# Remote state (recommended for teams)
# Use Azure Storage Backend
```

## Troubleshooting

### Common Issues

**1. Authentication Error**

```bash
# Error: Error building AzureRM Client: obtaining credentials for azure cli

# Solution:
az logout
az login
az account set --subscription <subscription-id>
```

**2. Insufficient Quota**

```bash
# Error: Code="InvalidTemplateDeployment" Message="The template deployment failed..."

# Solution: Check quota limits
az compute vm list-usage --location eastus

# Request quota increase in Azure Portal
```

**3. Kubernetes Version Not Supported**

```bash
# Error: Kubernetes version not supported

# Solution: Use supported version
az aks get-versions --location eastus --output table

# Update kubernetes_version in terraform.tfvars
```

**4. Network Policy Conflicts**

```bash
# Error: Network policy deployment failed

# Solution: Check NSG rules
az network nsg show --resource-group <rg> --name <nsg-name>

# Verify rules allow necessary traffic
```

### Debugging

```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform apply

# Check Azure resources
az resource list --resource-group kazestack-rg

# Check AKS cluster status
az aks show --resource-group kazestack-rg --name kazestack-cluster

# Check node status
kubectl get nodes -o wide
kubectl describe node <node-name>
```

## Cost Optimization

### Estimate Costs

```bash
# Before applying, review pricing:
# - AKS (managed service): ~$70/month cluster
# - Compute (Standard_D2s_v3 x 3): ~$300/month
# - Network: ~$30/month
# - Storage: ~$5/month
# Total: ~$400/month

# Use Azure Calculator: https://azure.microsoft.com/en-us/pricing/calculator/
```

### Cost Reduction Tips

1. **Use Spot Instances**

   ```hcl
   vm_priority = "Spot"  # Cheaper but interruptible
   ```

2. **Auto-scaling**
   - Scale nodes based on demand
   - Use cluster autoscaler

3. **Right-sizing**
   - Choose appropriate VM size
   - Monitor actual usage

4. **Reserved Instances**
   - Commit to 1-year or 3-year terms
   - Significant discounts

5. **Stop Cluster When Not Needed**
   ```bash
   az aks stop --resource-group kazestack-rg --name kazestack-cluster
   az aks start --resource-group kazestack-rg --name kazestack-cluster
   ```

## Advanced Topics

### Custom Node Pools

```hcl
# Add additional node pool for specific workloads
resource "azurerm_kubernetes_cluster_node_pool" "gpu" {
  name                  = "gpu"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  node_count            = 1
  vm_size               = "Standard_NC6s_v3"
}
```

### Private Cluster

```hcl
# Make cluster private (no public endpoint)
private_cluster_enabled = true
authorized_ip_ranges    = ["YOUR.IP.ADDRESS/32"]
```

### Multiple Regions

```bash
# Deploy to multiple regions for HA
# Use multiple terraform state files or Terraform Cloud
terraform workspace new us-east
terraform workspace new eu-west
```

## Security Best Practices

1. **Network Security**
   - Use Network Policies
   - Restrict NSG rules
   - Enable WAF on Ingress

2. **Access Control**
   - Use RBAC
   - Enable Azure AD integration
   - Service principals with minimal permissions

3. **Data Protection**
   - Enable Azure Disk Encryption
   - Use Azure Key Vault for secrets
   - Enable audit logging

4. **Monitoring**
   - Enable Azure Monitor
   - Set up alerts
   - Review security recommendations

## Support & Resources

- [Terraform AzureRM Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Kubernetes Service Docs](https://learn.microsoft.com/en-us/azure/aks/)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices.html)
- [AKS Security Best Practices](https://learn.microsoft.com/en-us/azure/aks/concepts-security)

---

For issues or questions, please refer to [CONTRIBUTING.md](../../CONTRIBUTING.md)
