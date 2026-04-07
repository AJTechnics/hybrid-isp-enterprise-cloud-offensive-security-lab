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

resource "proxmox_virtual_environment_vm" "ubuntu_test" {
  name      = "ubuntu-test-01"
  node_name = "pve"

  clone {
    vm_id = 101
  }

  cpu {
    cores = 2
  }

  memory {
    dedicated = 2048
  }

  disk {
    datastore_id = "vmdata"
    interface    = "scsi0"
    size         = 60
  }

  network_device {
    bridge = "vmbr0"
  }
}
