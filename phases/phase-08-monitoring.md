# Phase 08 — Monitoring and Operations Maturity

## Goal

Treat the lab like an operational environment. Deploy monitoring and build visibility into the lab's health.

## Scope

mon1: monitoring stack, service checks, dashboards.

## Components

- mon1 — monitoring node
- Logging or basic observability
- Dashboards and availability checks

## Tasks

- [ ] Deploy mon1
- [ ] Choose monitoring stack (Prometheus + Grafana, Zabbix, Checkmk, or similar)
- [ ] Add critical nodes to monitoring (routers, firewall, AD, app, LB)
- [ ] Configure availability checks (ICMP, TCP port checks)
- [ ] Configure alerting thresholds
- [ ] Build a basic dashboard for lab overview
- [ ] Create incident notes template
- [ ] Configure log collection for key services (optional)
- [ ] Document operational runbook for lab

## Topics

- Availability monitoring
- Service checks (ICMP, TCP, HTTP)
- Route and service dependency thinking
- Operational visibility and dashboards
- Incident management workflow

## Risks / Blockers

- mon1 needs visibility to all segments — firewall rules must allow monitoring traffic
- Monitoring stack choice affects resource usage

## Validation

- Important lab services are monitored
- A simulated failure is detected by monitoring
- Operational workflow is documented

## Notes

- Start simple: ICMP and TCP checks before full telemetry
- Define monitoring scope early — not everything needs to be monitored deeply
- Use this phase to build an operations mindset, not just a tool deployment

## Exit Criteria

- Important services are monitored
- Failures are visible quickly
- Operational workflow is improving
