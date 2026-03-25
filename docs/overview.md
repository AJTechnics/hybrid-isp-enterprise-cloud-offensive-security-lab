# Project Overview

## Summary

This lab simulates a full-stack environment spanning ISP/provider networking, enterprise infrastructure, cloud integration, and offensive security. It is built in phases on Proxmox and designed to be documented, explainable, and shareable.

## Project Vision

This lab is a personal platform to rebuild deep technical capability across provider networking, enterprise infrastructure, cloud connectivity, offensive security, and automation. It is designed as a phased environment that grows from a routing foundation into a hybrid operational platform that can be documented, explained, tested, and eventually shared with a study group.

## What This Lab Simulates

- An ISP core and edge network
- A customer enterprise environment
- Load balancing and application delivery
- Identity services with Active Directory
- A cloud extension into AWS
- An offensive security segment
- A Source of Truth and automation platform

## Build Principles

1. Build in phases, not all at once
2. Prefer simple and working over complex and unfinished
3. Document every design decision
4. Treat the lab like a real customer environment
5. Use the lab to explain, teach, and troubleshoot
6. Automate only after the manual process is understood

## Success Criteria

- Explain the end-to-end traffic path from user to application
- Deploy and troubleshoot the network without guessing
- Simulate provider and enterprise routing domains
- Expose and protect services through firewall and load balancer layers
- Extend the environment into AWS
- Test attack paths from an offensive security segment
- Document the design clearly enough for others to follow
- Use NetBox and automation to track and change the environment

## Related Files

- [`../homelab_lab_blueprint.md`](../homelab_lab_blueprint.md) — full original blueprint
- [`topology.md`](topology.md) — logical topology and routing domains
- [`goals.md`](goals.md) — detailed goal breakdown
