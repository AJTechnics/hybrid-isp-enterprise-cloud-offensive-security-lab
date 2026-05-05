terraform {
  required_providers {
    proxmox = {
      source = "bpg/proxmox"
    }
  }
}

resource "proxmox_virtual_environment_vm" "this" {
  name      = var.name
  node_name = var.node_name
  vm_id     = var.vm_id

  clone {
    vm_id     = var.template_vm_id
    node_name = var.clone_node_name
  }

  cpu {
    cores = var.cpu_cores
  }

  memory {
    dedicated = var.memory_mb
  }

  disk {
    datastore_id = var.datastore_id
    interface    = "scsi0"
    size         = var.disk_size_gb
  }

  dynamic "network_device" {
    for_each = var.network_bridges
    content {
      bridge = network_device.value
    }
  }

  dynamic "initialization" {
    for_each = var.initialization_datastore_id != null ? [1] : []
    content {
      datastore_id = var.initialization_datastore_id

      dynamic "user_account" {
        for_each = var.initialization_user != null ? [1] : []
        content {
          username = var.initialization_user
          password = var.initialization_password
          keys     = var.initialization_ssh_keys
        }
      }

      dynamic "ip_config" {
        for_each = var.initialization_ipv4_address != null ? [1] : []
        content {
          ipv4 {
            address = var.initialization_ipv4_address
            gateway = var.initialization_ipv4_gateway
          }
        }
      }

      dynamic "dns" {
        for_each = length(var.initialization_dns_servers) > 0 ? [1] : []
        content {
          servers = var.initialization_dns_servers
        }
      }
    }
  }
}


