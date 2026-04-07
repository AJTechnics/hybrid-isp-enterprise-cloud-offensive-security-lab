##  Build Log — OpenTofu First VM Deployment

###  Date
2026-04-07

###  Objective
Deploy first VM in Proxmox using OpenTofu (Infrastructure as Code) instead of manual provisioning.

---

## Environment

- Host: `ws1` (Ubuntu workspace VM)
- Runtime: Podman container (`lab-toolbox`)
- Provisioning tool: OpenTofu
- Provider: `bpg/proxmox`
- Proxmox node: `pve`
- Storage: `vmdata`
- Network bridge: `vmbr0`

---

## Steps Taken

### 1. Enter toolbox container

```bash
podman run --rm -it \
  -v ~/workspace:/workspace \
  localhost/lab-toolbox

## 2. Navigate to OpenTofu environment

cd /file/path/here

## 3. Confiure OpenTofu files
main.tf
- Defined provider (bpg/proxmox)
- Added VM resource using template clone
variables.tf
- Defined:
	- proxmox_api_url
	- proxmox_username
	- proxmox_password
terraform.tfvars
- Stored actual values (NOT committed to Git)

## 4. Initalize OpenTofu
-#Command# tofu init

Result:
- Provider downloaded
- .terraform.lock.hcl created

## 5. Validate configuration
-#Command# tofu validate

Resulte: 
- Configuration valid

## 6. Plan deployment

Command# tofu plan

Result: 
- VM creation detected

## 7. Apply Deployment

Command# tofu apply

## Issues Encountered
Issue 1 - Authentication timeout
Error:
	Failed to authenticate: contect deadline exceeded
Cause:
 - Temporary connectivity/API issue to proxmox

Resolution:
 - Retried apply
 
Issue 2 - Disk resize failure
 Error: 
	Requested size (20G) is lower than current size (60G)
 
Cause:
 - Template disksize was 60G
 - Config requested smaller disk
 
Resolution:
 - Re-applied after replacing config (20G) -> (60G)
 - VM created succesfully

## Result
- VM successfully deployed via OpenTofu
- VM ID: 102
- Name: ubuntu-test-01
- Node: pve
- Storage: vmdata
- Network: vmbr0
- Clone source: template VMID 101

## Key Learnings
- OpenTofu runs inside container, not host
-Separation of:
- main.tf → resources
- variables.tf → definitions
- terraform.tfvars → secrets
- Provider/resource mismatch can break deployments
- Template disk size must not be reduced
- Infrastructure can now be reproducible via code

## Next steps
- Convert VM config into reusable module
- Start building core network nodes(ISP/Routers)
- Integrate Anisble for post-deployment config

