variable "location" {
  description = "Azure region der alle ressurser opprettes"
  type        = string
  default     = "norwayeast"
}

variable "project" {
  description = "Prosjektnavn — brukes som prefix på alle ressursnavn"
  type        = string
  default     = "platform-p3"
}

variable "environment" {
  description = "Miljønavn (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aks_node_count" {
  description = "Antall noder i AKS-clusteret"
  type        = number
  default     = 2
}

variable "aks_node_size" {
  description = "VM-størrelse for AKS-noder"
  type        = string
  default     = "Standard_B2s"
}
