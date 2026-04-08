terraform {
  required_version = ">= 1.6.0"

  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "~> 0.66"
    }
  }
}

provider "proxmox" {
  endpoint = var.proxmox_api_url
  username = var.proxmox_username
  password = var.proxmox_password
  insecure = true
}

module "isp_core1" {
  source         = "../../modules/proxmox-vm"
  name           = "isp-core1"
  node_name      = "pve"
  template_vm_id = 101
  datastore_id   = "vmdata"
  bridge         = "vmbr0"
  cpu_cores      = 2
  memory_mb      = 2048
  disk_size_gb   = 60
}

module "isp_core2" {
  source         = "../../modules/proxmox-vm"
  name           = "isp-core2"
  node_name      = "pve"
  template_vm_id = 101
  datastore_id   = "vmdata"
  bridge         = "vmbr0"
  cpu_cores      = 2
  memory_mb      = 2048
  disk_size_gb   = 60
}

module "pe1" {
  source         = "../../modules/proxmox-vm"
  name           = "pe1"
  node_name      = "pve"
  template_vm_id = 101
  datastore_id   = "vmdata"
  bridge         = "vmbr0"
  cpu_cores      = 2
  memory_mb      = 2048
  disk_size_gb   = 60
}

module "ce1" {
  source         = "../../modules/proxmox-vm"
  name           = "ce1"
  node_name      = "pve"
  template_vm_id = 101
  datastore_id   = "vmdata"
  bridge         = "vmbr0"
  cpu_cores      = 2
  memory_mb      = 2048
  disk_size_gb   = 60
}
