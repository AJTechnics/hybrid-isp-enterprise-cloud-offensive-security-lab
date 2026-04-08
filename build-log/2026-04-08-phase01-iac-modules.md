#  2026-04-08 — Phase 01 IaC Modularization

## Objective

Transition from single VM deployment to reusable Infrastructure-as-Code for Phase 01 network nodes.

---

## Steps Taken

### 1. Fixed OpenTofu Configuration Issues

* Incorrect use of `terraform.tfvars` (contained resource blocks)
* Invalid variable names (URLs/passwords used as variable names)
* Missing provider declaration inside module

### 2. Provider Fix

Added required provider to module:

```hcl
terraform {
  required_providers {
    proxmox = {
      source = "bpg/proxmox"
    }
  }
}
```

---

### 3. Created Reusable Module

Path:

```text
opentofu/modules/proxmox-vm/
```

Components:

* `main.tf`
* `variables.tf`
* `outputs.tf`

Capabilities:

* Clone from template
* Configure CPU, memory, disk
* Attach network interface

---

### 4. Refactored Environment

Replaced single VM resource with module usage:

```hcl
module "isp_core1" { ... }
module "isp_core2" { ... }
module "pe1" { ... }
module "ce1" { ... }
```

---

### 5. Deployment

Executed:

```bash
tofu init -upgrade
tofu validate
tofu plan
tofu apply
```

Result:

* Destroyed: `ubuntu-test-01`
* Created:

  * isp-core1
  * isp-core2
  * pe1
  * ce1

---

## Key Insights

* Modules are required for scaling infrastructure cleanly
* Provider declarations must exist in each module
* OpenTofu state enforces desired state strictly (removed unmanaged resources)
* Separation of concerns:

  * Template → OS baseline
  * OpenTofu → provisioning
  * Future (Ansible) → configuration

---

## Current Limitations

* All VMs attached to `vmbr0`
* No multi-interface topology yet
* No routing or network roles configured

---

## Next Steps

1. Extend module to support multiple NICs
2. Map Proxmox bridges to network topology
3. Introduce router-specific templates (VyOS)
4. Deploy NetBox for network source of truth
5. Integrate OpenTofu with NetBox (future)

---
