variable "name" {
  type = string
}

variable "node_name" {
  type = string
}

variable "template_vm_id" {
  type = number
}

variable "datastore_id" {
  type = string
}

variable "bridge" {
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
