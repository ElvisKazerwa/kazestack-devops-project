# Terraform - Azure Infrastructure as Code

Production-grade Terraform configuration for deploying K8s-App to Azure Kubernetes Service (AKS).

## Architecture

This Terraform configuration provisions:

- **Azure Kubernetes Service (AKS)** - Managed Kubernetes cluster with autoscaling
- **Azure Container Registry (ACR)** - Private Docker image registry
- **Virtual Network** - Network isolation with subnets and NSGs
- **Log Analytics & Application Insights** - Monitoring and logging
- **Public IP** - For ingress controller
- **RBAC & Managed Identity** - Secure access control

## Prerequisites

1. **Azure CLI** installed and configured
   ```bash
   az login
   az account set --subscription <subscription-id>
   ```

2. **Terraform** >= 1.0
   ```bash
   terraform version
   ```

3. **kubectl** for Kubernetes management
   ```bash
   kubectl version --client
   ```

## File Structure

```
terraform-azure/
├── versions.tf           # Provider versions and requirements
├── variables.tf          # Input variable definitions
├── locals.tf             # Local variables
├── main.tf               # Main infrastructure resources
├── outputs.tf            # Output values
├── terraform.tfvars.example  # Example variables file
└── README.md             # This file
```

## Configuration

### 1. Create terraform.tfvars

Copy the example and customize:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your settings:

```hcl
environment          = "prod"
location             = "West Europe"
resource_group_name  = "k8s-app-prod-rg"
project_name         = "k8sapp"
node_count           = 3
max_node_count       = 10
node_vm_size         = "Standard_B2s"
```

### 2. Key Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `environment` | "prod" | Environment (dev, staging, prod) |
| `location` | "West Europe" | Azure region |
| `kubernetes_version` | "1.27" | Kubernetes version |
| `node_count` | 3 | Initial node count |
| `max_node_count` | 10 | Max nodes for autoscaling |
| `node_vm_size` | "Standard_B2s" | VM size for nodes |
| `acr_sku` | "Standard" | Container Registry tier |
| `enable_monitoring` | true | Enable monitoring |

## Usage

### Initialize Terraform

```bash
cd terraform-azure
terraform init
```

### Plan Deployment

```bash
terraform plan -out=tfplan
```

Review the plan to ensure correct resources will be created.

### Apply Configuration

```bash
terraform apply tfplan
```

This will create all infrastructure in Azure.

### Get Outputs

```bash
terraform output

# Get specific values
terraform output -json aks_cluster_name
terraform output ingress_public_ip
```

## Post-Deployment

### Configure kubectl

```bash
az aks get-credentials \
  --resource-group k8s-app-prod-rg \
  --name k8sapp-aks \
  --admin
```

Or use the Terraform output:

```bash
$(terraform output -raw command_configure_kubectl)
```

### Verify Kubernetes Cluster

```bash
kubectl cluster-info
kubectl get nodes
kubectl get namespaces
```

### Deploy K8s-App

```bash
cd ../k8s
kubectl apply -f . -n production
kubectl get pods -n production
```

## Remote State Management (Optional)

For team collaboration, use remote state storage:

### 1. Create Storage Account

```bash
az storage account create \
  --name terraformstate \
  --resource-group terraform-state-rg \
  --location "West Europe"

az storage container create \
  --name tfstate \
  --account-name terraformstate
```

### 2. Update versions.tf

Uncomment the backend configuration in `versions.tf`:

```hcl
backend "azurerm" {
  resource_group_name  = "terraform-state-rg"
  storage_account_name = "terraformstate"
  container_name       = "tfstate"
  key                  = "k8s-app.tfstate"
}
```

### 3. Re-initialize Terraform

```bash
terraform init
```

## Monitoring & Logging

The configuration includes:

- **Log Analytics Workspace** - Centralized logging
- **Application Insights** - Performance monitoring
- **Diagnostic Settings** - AKS cluster diagnostics
- **Prometheus** - Application metrics

Access monitoring:

```bash
# View AKS logs
kubectl logs deployment/k8s-app -n production

# Check HPA status
kubectl get hpa -n production

# Port forward to Prometheus
kubectl port-forward -n kube-system svc/prometheus 9090:9090
```

## Scaling

### Horizontal Pod Autoscaling

Configured in `k8s/hpa.yml` (3-10 replicas based on CPU/Memory)

### Vertical Scaling (Node Pool)

Update `terraform.tfvars`:

```hcl
node_vm_size   = "Standard_B4ms"  # Larger VM
max_node_count = 20               # More nodes
```

Then apply:

```bash
terraform plan
terraform apply
```

## Destruction

⚠️ **Warning**: This will delete all resources in the cluster.

```bash
# Destroy infrastructure
terraform destroy
```

## Security Best Practices

✅ Implemented:
- Non-root container users
- Network policies (Azure CNI)
- RBAC with Managed Identity
- Private ACR with AKS integration
- Network Security Groups
- Azure AD integration (ready)

## Troubleshooting

### Cannot create AKS cluster

```bash
# Check resource group exists
az group show -n k8s-app-prod-rg

# Check provider registration
az provider register --namespace Microsoft.ContainerService
az provider register --namespace Microsoft.Network
```

### kubectl connection fails

```bash
# Re-authenticate
az aks get-credentials --resource-group <rg-name> --name <aks-name> --overwrite-existing

# Check context
kubectl config current-context
kubectl config get-contexts
```

### State file locked

```bash
# Release state lock (use carefully)
terraform force-unlock <LOCK_ID>
```

## Cost Optimization

- Use `Standard_B2s` for dev/test
- Reduce `max_node_count` in dev environments
- Use `Free` tier for `aks_sku_tier` in dev
- Disable monitoring in test environments

Example dev configuration:

```hcl
environment        = "dev"
aks_sku_tier       = "Free"
node_count         = 1
max_node_count     = 3
node_vm_size       = "Standard_B1s"
enable_monitoring  = false
```

## CI/CD Integration

GitHub Actions workflow can automate Terraform:

```yaml
- name: Terraform Plan
  run: |
    cd terraform-azure
    terraform init
    terraform plan -out=tfplan

- name: Terraform Apply
  run: |
    cd terraform-azure
    terraform apply tfplan
```

## Support

For issues, check:
- [Terraform Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [AKS Best Practices](https://docs.microsoft.com/en-us/azure/aks/best-practices)
