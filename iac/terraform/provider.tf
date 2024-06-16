terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "0.50.0" # x-release-please-version
    }
  }
}

provider "proxmox" {
  endpoint  = var.virtual_environment_endpoint
  api_token = var.virtual_environment_token
  insecure  = true
  ssh {
    agent    = true
    username = var.virtual_environment_ssh_username
    password = var.virtual_environment_ssh_password
  }
}
