# Architecture Documentation

## Overview

This project deploys a containerized Python application on Azure Kubernetes Service (AKS) with infrastructure defined as code.

## Components

- **Application**: Python-based service in `app/kazestack-devops-project/`
- **Infrastructure**: Terraform and Kubernetes manifests for Azure deployment
- **CI/CD**: Azure Pipelines for automated build and deployment

## Data Flow

1. Code pushed to GitHub
2. Azure Pipeline triggers build
3. Docker image created and pushed to container registry
4. Kubernetes deployment updated with new image
5. Application runs on AKS
