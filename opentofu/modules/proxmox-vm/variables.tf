variable "name" {
  type = string
}

variable "vm_id" {
  type    = number
  default = null
}

variable "node_name" {
  type = string
}

variable "template_vm_id" {
  type = number
}

variable "clone_node_name" {
  type    = string
  default = null
}

variable "datastore_id" {
  type = string
}

variable "cpu_cores" {
  type    = number
  default = 2
}

variable "memory_mb" {
  type    = number
  default = 2048
}

variable "disk_size_gb" {
  type    = number
  default = 60
}

variable "network_bridges" {
  type = list(string)
}

variable "initialization_datastore_id" {
  type    = string
  default = null
}

variable "initialization_user" {
  type    = string
  default = null
}

variable "initialization_password" {
  type      = string
  default   = null
  sensitive = true
}

variable "initialization_ssh_keys" {
  type    = list(string)
  default = []
}

variable "initialization_ipv4_address" {
  type    = string
  default = null
}

variable "initialization_ipv4_gateway" {
  type    = string
  default = null
}

variable "initialization_dns_servers" {
  type    = list(string)
  default = []
}