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
  source          = "../../modules/proxmox-vm"
  name            = "isp-core1"
  node_name       = "pve-node1"
  template_vm_id  = 101
  datastore_id    = "vmdata"
  cpu_cores       = 2
  memory_mb       = 2048
  disk_size_gb    = 60
  network_bridges = ["vmbr2", "vmbr3", "vmbr5"]
}

module "isp_core2" {
  source          = "../../modules/proxmox-vm"
  name            = "isp-core2"
  node_name       = "pve-node1"
  template_vm_id  = 101
  datastore_id    = "vmdata"
  cpu_cores       = 2
  memory_mb       = 2048
  disk_size_gb    = 60
  network_bridges = ["vmbr2", "vmbr4"]
}

module "pe1" {
  source          = "../../modules/proxmox-vm"
  name            = "pe1"
  node_name       = "pve-node1"
  template_vm_id  = 101
  datastore_id    = "vmdata"
  cpu_cores       = 2
  memory_mb       = 2048
  disk_size_gb    = 60
  network_bridges = ["vmbr3", "vmbr4", "vmbr1"]
}

module "ce1" {
  source          = "../../modules/proxmox-vm"
  name            = "ce1"
  node_name       = "pve-node1"
  template_vm_id  = 101
  datastore_id    = "vmdata"
  cpu_cores       = 2
  memory_mb       = 2048
  disk_size_gb    = 60
  network_bridges = ["vmbr1"]
}

module "svc1" {
  source          = "../../modules/proxmox-vm"
  name            = "svc1"
  node_name       = "pve-node1"
  template_vm_id  = 101
  datastore_id    = "vmdata"
  cpu_cores       = 2
  memory_mb       = 4096
  disk_size_gb    = 60
  network_bridges = ["vmbr0"]
}

module "media1" {
  source          = "../../modules/proxmox-vm"
  name            = "media1"
  node_name       = "pve-node2"
  template_vm_id  = 201
  datastore_id    = "local-lvm"
  cpu_cores       = 4
  memory_mb       = 8192
  disk_size_gb    = 100
  network_bridges = ["vmbr0"]
}

module "media2" {
  source                      = "../../modules/proxmox-vm"
  name                        = "media2"
  vm_id                       = 109
  node_name                   = "pve-node3"
  template_vm_id              = 201
  clone_node_name             = "pve-node2"
  datastore_id                = "local-lvm"
  cpu_cores                   = 4
  memory_mb                   = 8192
  disk_size_gb                = 100
  network_bridges             = ["vmbr0"]
  initialization_datastore_id = "local-lvm"
  initialization_user         = "lab"
  initialization_password     = var.media2_bootstrap_password
  initialization_ssh_keys     = [trimspace(file("~/.ssh/id_ed25519.pub"))]
  initialization_ipv4_address = "192.168.1.133/24"
  initialization_ipv4_gateway = "192.168.1.1"
  initialization_dns_servers  = ["192.168.1.1"]
}



