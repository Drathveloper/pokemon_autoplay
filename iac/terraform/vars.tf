variable "virtual_environment_endpoint" {
  type        = string
  description = "The endpoint for the Proxmox Virtual Environment API (example: https://host:port)"
}

variable "virtual_environment_token" {
  type        = string
  description = "The token for the Proxmox Virtual Environment API"
}

variable "virtual_environment_ssh_username" {
  type        = string
  description = "The ssh username for the Proxmox Virtual Environment API"
}

variable "virtual_environment_ssh_password" {
  type = string
  description = "The ssh password for the Proxmox Virtual Environment API"
}

variable "node1_id" {
  type        = string
  description = "The node 1 id"
}

variable "node2_id" {
  type        = string
  description = "The node 2 id"
}

variable "node3_id" {
  type        = string
  description = "The node 3 id"
}
