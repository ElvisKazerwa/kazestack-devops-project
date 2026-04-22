# Deployment script for Windows PowerShell
# Usage: .\deploy.ps1 -Environment dev -Region eastus

param(
    [string]$Environment = "dev",
    [string]$Region = "eastus"
)

$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deploying to $Environment environment" -ForegroundColor Cyan
Write-Host "Region: $Region" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

# Deploy Terraform
Write-Host ""
Write-Host "[1/2] Applying Terraform configuration..." -ForegroundColor Yellow
Push-Location "$RepoRoot\infra\terraform\envs\$Environment"

try {
    terraform init
    terraform plan -out=tfplan
    terraform apply tfplan
} finally {
    Pop-Location
}

# Deploy Kubernetes
Write-Host ""
Write-Host "[2/2] Deploying Kubernetes manifests..." -ForegroundColor Yellow
Push-Location $RepoRoot

try {
    kubectl apply -k "infra\k8s\overlays\$Environment\"
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
