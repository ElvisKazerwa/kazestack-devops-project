##########################################
# Resource Group
##########################################

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = local.tags
}

##########################################
# Virtual Network
##########################################

resource "azurerm_virtual_network" "vnet" {
  name                = "${local.base_name}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  address_space = [
    "10.1.0.0/16"
  ]

  tags = local.tags
}

##########################################
# AKS Subnet
##########################################

resource "azurerm_subnet" "aks" {
  name                 = "${local.base_name}-aks-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name

  address_prefixes = [
    "10.1.1.0/24"
  ]
}

##########################################
# NSG
##########################################

resource "azurerm_network_security_group" "aks_nsg" {
  name                = "${local.base_name}-aks-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  tags = local.tags

  security_rule {
    name      = "AllowHttps"
    priority  = 100
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "443"

    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name      = "AllowHttp"
    priority  = 101
    direction = "Inbound"
    access    = "Allow"
    protocol  = "Tcp"

    source_port_range      = "*"
    destination_port_range = "80"

    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "aks" {
  subnet_id                 = azurerm_subnet.aks.id
  network_security_group_id = azurerm_network_security_group.aks_nsg.id
}

##########################################
# User Assigned Identity
##########################################

resource "azurerm_user_assigned_identity" "aks" {
  name                = "${local.base_name}-aks-mi"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  tags = local.tags
}

##########################################
# AKS
##########################################

resource "azurerm_kubernetes_cluster" "aks" {

  name                = "${local.base_name}-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  dns_prefix         = local.base_name
  kubernetes_version = var.kubernetes_version
  sku_tier           = var.aks_sku_tier

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  tags = local.tags

  default_node_pool {
    name       = "default"
    vm_size    = var.node_vm_size
    node_count = var.node_count

    enable_auto_scaling = true
    min_count           = var.min_node_count
    max_count           = var.max_node_count

    os_disk_size_gb = 128

    type = "VirtualMachineScaleSets"

    zones = ["1", "2", "3"]

    vnet_subnet_id = azurerm_subnet.aks.id

    tags = local.tags
  }

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.aks.id
    ]
  }

  network_profile {

    network_plugin = "azure"
    network_policy = "azure"

    # Must not overlap VNET CIDR
    service_cidr   = "10.2.0.0/16"
    dns_service_ip = "10.2.0.10"

    load_balancer_sku = "standard"
  }

  depends_on = [
    azurerm_subnet_network_security_group_association.aks
  ]
}

##########################################
# ACR
##########################################

resource "azurerm_container_registry" "acr" {

  name = replace(
    "${local.base_name}acr",
    "-",
    ""
  )

  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku           = var.acr_sku
  admin_enabled = false

  tags = local.tags
}

##########################################
# ACR Pull Rights
##########################################

resource "azurerm_role_assignment" "aks_acr_pull" {

  scope = azurerm_container_registry.acr.id

  role_definition_name = "AcrPull"

  # Better than UAMI principal for pulls
  principal_id = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}

##########################################
# Log Analytics
##########################################

resource "azurerm_log_analytics_workspace" "law" {
  count = var.enable_monitoring ? 1 : 0

  name                = "${local.base_name}-law"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku               = "PerGB2018"
  retention_in_days = var.log_retention_days

  tags = local.tags
}

##########################################
# Application Insights
##########################################

resource "azurerm_application_insights" "ai" {
  count = var.enable_monitoring ? 1 : 0

  name                = "${local.base_name}-ai"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  application_type = "web"

  workspace_id = azurerm_log_analytics_workspace.law[0].id

  tags = local.tags
}

##########################################
# AKS Diagnostics
##########################################

resource "azurerm_monitor_diagnostic_setting" "aks" {
  count = var.enable_monitoring ? 1 : 0

  name                       = "${local.base_name}-diag"
  target_resource_id         = azurerm_kubernetes_cluster.aks.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law[0].id

  enabled_log {
    category = "kube-apiserver"
  }

  enabled_log {
    category = "kube-controller-manager"
  }

  enabled_log {
    category = "kube-scheduler"
  }

  enabled_log {
    category = "kube-audit"
  }

  metric {
    category = "AllMetrics"
  }
}

##########################################
# Public IP
##########################################

resource "azurerm_public_ip" "ingress" {

  name                = "${local.base_name}-ingress-pip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  allocation_method = "Static"
  sku               = "Standard"

  tags = local.tags
}

##########################################
# Kubernetes Namespace
##########################################

resource "kubernetes_namespace" "production" {

  metadata {
    name = local.k8s_namespace

    labels = {
      name = local.k8s_namespace
    }
  }

  depends_on = [
    azurerm_kubernetes_cluster.aks
  ]
}
