terraform {
  required_version = ">= 1.7"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.110"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-platform-state"
    storage_account_name = "stplatp31e6c44c4"
    container_name       = "tfstate"
    key                  = "platform-stack-p3.tfstate"
  }
}

provider "azurerm" {
  features {}
}
