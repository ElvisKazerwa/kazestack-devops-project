# Kazestack DevOps Project

A comprehensive DevOps infrastructure-as-code project for deploying applications on Azure Kubernetes Service (AKS).

## Project Structure

```
repo-root/
├── app/                        # Application source code
│   ├── src/                    # Source code
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── deployment.yaml
│   ├── service.yaml
│   └── Dockerfile
├── infra/                      # Infrastructure definitions
│   ├── terraform/              # Infrastructure-as-Code (Terraform)
│   │   ├── modules/            # Reusable Terraform modules
│   │   └── envs/               # Environment-specific configs
│   │       ├── dev/
│   │       └── prod/
│   └── k8s/                    # Kubernetes manifests
│       ├── base/               # Base manifests
│       └── overlays/           # Kustomize overlays
│           ├── dev/
│           └── prod/
├── pipelines/                  # CI/CD pipelines
│   └── azure-pipelines.yml
├── scripts/                    # Deployment and utility scripts
│   ├── deploy.ps1
│   └── deploy.sh
├── docs/                       # Documentation
│   ├── architecture.md
│   ├── deployment.md
│   └── troubleshooting.md
├── .github/                    # GitHub configurations
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Getting Started

### Prerequisites

- Azure CLI
- Terraform
- kubectl
- Docker (optional)

### Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd kazestack-devops-project

# Set up infrastructure
cd infra/terraform/envs/dev
terraform init
terraform plan
terraform apply
```

### Deployment

Refer to [Deployment Guide](docs/deployment.md) for detailed instructions.

## Documentation

- [Architecture](docs/architecture.md) - System architecture and design
- [Deployment](docs/deployment.md) - Deployment procedures
- [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## Project Status

Current branch: features/K8s-app

## License

[Add your license here]
