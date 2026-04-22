locals {
  # Environment-specific configurations
  env_suffix = var.environment == "prod" ? "" : "-${var.environment}"
  
  # Resource naming convention
  base_name = "${var.project_name}${local.env_suffix}"
  
  # Kubernetes namespace
  k8s_namespace = "production"
  
  # Common tags
  tags = merge(
    var.common_tags,
    {
      Environment = var.environment
      CreatedAt   = timestamp()
    }
  )
}
