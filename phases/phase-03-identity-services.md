# Phase 03 — Identity and Core Enterprise Services

## Goal

Add the real enterprise backbone: Active Directory, DNS, and supporting Linux services.

## Scope

SERVER segment: Windows AD/DNS, Linux app server, test client in CLIENT segment.

## Components

- win-ad1 — Windows Server (Active Directory, DNS, optional DHCP)
- app1 — Linux application server
- Test client VM (CLIENT segment)

## Tasks

- [ ] Deploy win-ad1 (Windows Server)
- [ ] Configure Active Directory domain
- [ ] Configure DNS on win-ad1
- [ ] Configure DHCP if required
- [ ] Deploy app1 (Linux)
- [ ] Deploy test client VM
- [ ] Join test client to domain
- [ ] Configure firewall rules to allow AD and DNS traffic
- [ ] Verify client can authenticate to domain
- [ ] Verify DNS resolution works correctly
- [ ] Deploy and verify app1 is reachable through intended path
- [ ] Document DNS records and domain design
- [ ] Document service reachability matrix

## Topics

- Domain design
- DNS dependency mapping
- Domain join procedure
- Service reachability through firewall
- Troubleshooting authentication and name resolution

## Risks / Blockers

- Phase 2 must be complete (firewall and segmentation must be in place)
- Windows Server licensing / evaluation image required
- DNS must be working before domain join can succeed

## Validation

- Test client can authenticate to domain
- DNS resolves internal names correctly
- App server is reachable from CLIENT segment through correct path
- Firewall rules are explicit (not over-permissive)

## Notes

- Use evaluation/trial Windows Server ISO
- Document DNS forwarder config (internal vs external resolution)
- Map out which ports AD/DNS/Kerberos require and open them deliberately

## Exit Criteria

- Client can authenticate to the domain
- DNS works correctly for internal resolution
- App is reachable through the intended path
