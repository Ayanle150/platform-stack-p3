output "resource_group_name" {
  description = "Navn på resource group"
  value       = azurerm_resource_group.main.name
}

output "acr_login_server" {
  description = "ACR login server — brukes i docker push og Helm"
  value       = azurerm_container_registry.main.login_server
}

output "aks_cluster_name" {
  description = "AKS cluster-navn"
  value       = azurerm_kubernetes_cluster.main.name
}

output "aks_get_credentials" {
  description = "Kommando for å koble kubectl til clusteret"
  value       = "az aks get-credentials --resource-group ${azurerm_resource_group.main.name} --name ${azurerm_kubernetes_cluster.main.name}"
}

output "key_vault_name" {
  description = "Navn på Key Vault"
  value       = azurerm_key_vault.main.name
}
