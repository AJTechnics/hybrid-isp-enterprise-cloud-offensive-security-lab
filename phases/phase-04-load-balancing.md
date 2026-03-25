# Phase 04 — Load Balancing and Application Delivery

## Goal

Place an application behind a load-balancing layer in the DMZ. Build and validate the request path from client to VIP to backend.

## Scope

DMZ segment: lb1 (HAProxy), one or more backend app instances.

## Components

- lb1 — load balancer (HAProxy)
- One or more backend application servers
- DMZ exposure pattern

## Tasks

- [ ] Deploy lb1 (HAProxy)
- [ ] Configure L4 frontend and backend pool
- [ ] Configure L7 frontend (HTTP/HTTPS)
- [ ] Configure health checks on backend pool
- [ ] Configure TLS termination (self-signed cert initially)
- [ ] Place application(s) behind load balancer
- [ ] Test VIP reachability from CLIENT segment
- [ ] Test backend failover behaviour
- [ ] Configure persistence / session stickiness
- [ ] Document full request path
- [ ] Create F5 concept mapping notes

## Topics

- L4 vs L7 load balancing
- Health checks and backend pool management
- TLS termination
- Reverse proxying
- Persistence and session stickiness
- F5 terminology mapping (VIP, pool, node, iRule equivalents)

## Risks / Blockers

- Phase 3 must be complete (app server must exist)
- Phase 2 must be complete (DMZ segment must be ready)
- TLS certificate management for lab (self-signed acceptable)

## Validation

- Application is reachable through lb1 VIP from CLIENT segment
- Failed backend is removed from pool and health check detects it
- Request path can be traced and explained end to end

## Notes

- Map HAProxy concepts to F5 equivalents after each config step
- Start with L4 pass-through before adding L7 features
- Document health check timing and thresholds

## Exit Criteria

- App is reachable through load balancer
- Failed backend behaviour is validated
- Full request path is documented and explainable
