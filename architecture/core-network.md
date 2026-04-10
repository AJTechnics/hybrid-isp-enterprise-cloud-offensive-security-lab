# Core Network Architecture

## Purpose

Phase 01 establishes the provider and customer edge foundation of the lab.
The goal is to move from generic VM deployment to a topology that supports
routing, traffic flow validation, and later automation.

## Phase Status

-  Phase 00 — Project Foundation completed
-  Phase 01 — ISP Core Edge in progress

## Scope of This Phase

This phase focuses on:

- provider/core network nodes
- PE/CE handoff
- multi-interface VM topology
- interface-to-bridge mapping
- preparation for routing and validation

This phase does not yet include:

- firewall services
- Active Directory
- load balancing
- AWS hybrid connectivity
- monitoring stack
- Kubernetes or GitLab deployment

## Nodes

The current Phase 01 node set is:

- `isp-core1`
- `isp-core2`
- `pe1`
- `ce1`

These nodes are deployed through OpenTofu using the reusable `proxmox-vm` module.

## Provisioning Model

Infrastructure is provisioned through:

- Proxmox as the hypervisor platform
- OpenTofu for VM lifecycle management
- Proxmox template cloning for repeatable deployment
- Git-based version control for infrastructure definitions

The current template source is:

- template VM ID: `101`

The current datastore is:

- `vmdata`

The current Proxmox node is:

- `pve`

## Logical Topology

```text
[ isp-core1 ] ----- [ isp-core2 ]
      |                  |
      |                  |
      +------ [ pe1 ] ---+
                 |
                 |
               [ ce1 ]
