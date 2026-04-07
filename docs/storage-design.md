# Storage Design

## Current layout

### Primary disk
- NVMe disk
- Used for Proxmox OS and default Proxmox storage

### Secondary disk
- Samsung SSD 850 PRO 512GB
- Configured as LVM-thin storage
- Storage name: `vmdata`

## Policy

All lab VMs must be deployed to `vmdata`.

## Reasoning

- keeps Proxmox system storage separate from lab workloads
- standardizes deployment targets for automation
- simplifies rebuilds and documentation


