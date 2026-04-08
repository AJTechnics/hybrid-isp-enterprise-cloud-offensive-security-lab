# Daily Build Log

Use one entry per session. Copy the template below for each new entry.

---

## Template

```markdown
## YYYY-MM-DD

**Phase:** Phase X — Name  
**Time spent:** ~Xh

### What I worked on

### What I changed

### What worked

### What failed

### What I learned

### Next step
```

---

## Entries

<!-- Add new log entries below, newest first -->

##  2026-04-08

### Summary

Major transition from single VM deployment to modular Infrastructure-as-Code (IaC) using OpenTofu.

### Work Completed

* Fixed OpenTofu provider issues (`bpg/proxmox`)
* Corrected variable definitions and configuration structure
* Successfully initialized and validated OpenTofu environment
* Created first reusable OpenTofu module (`proxmox-vm`)
* Refactored environment to use module-based deployments
* Deployed Phase 01 nodes:

  * isp-core1
  * isp-core2
  * pe1
  * ce1
* Removed initial test VM (`ubuntu-test-01`)
* Updated repository structure:

  * Added `opentofu/`
  * Added `architecture/`
  * Added `runbooks/`
* Updated phase tracking:

  * Phase 00 → Completed
  * Phase 01 → In Progress

### Key Learnings

* OpenTofu modules require explicit `required_providers`
* Separation of:

  * templates (base images)
  * IaC (provisioning)
  * configuration (future Ansible)
* Importance of clean repo structure for scaling lab complexity

### Next Steps

* Add multi-interface support to VM module
* Design core network topology (bridges + links)
* Introduce NetBox for source of truth
* Begin router-focused templates (VyOS)

---

## 2026-04-07

- Built first VM using OpenTofu + Proxmox (successful)
- Learned provider setup, cloning, and state handling
- Ran into disk size mismatch + API timeout (resolved)
- Next: modularize VM + start network nodes
## 2026-04-01

**Phase:** Phase 0 — Foundation
**Time spent:** ~30min

### What I worked on
Tested the lab-update script

### What I changed
Fixed script bugs

### What worked
Script runs correctly

### What failed
n/a

### What I learned
Always test scripts before committing

### Next step
Run full option 4 next session
