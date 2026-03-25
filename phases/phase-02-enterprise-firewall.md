# Phase 02 — Enterprise Firewall and Internal Segmentation

## Goal

Place a customer enterprise behind CE1. Build segmented internal zones controlled by a firewall.

## Scope

Customer domain: firewall, DMZ, SERVER, CLIENT, MGMT segments.

## Components

- fw1 — enterprise firewall (pfSense or OPNsense)
- VLAN-backed or logically separated internal networks
- DMZ segment
- SERVER segment
- CLIENT segment
- MGMT segment

## Tasks

- [ ] Deploy fw1
- [ ] Configure CE1-to-firewall routing
- [ ] Create DMZ segment and assign addressing
- [ ] Create SERVER segment and assign addressing
- [ ] Create CLIENT segment and assign addressing
- [ ] Create MGMT segment and assign addressing
- [ ] Configure firewall zones
- [ ] Configure baseline outbound NAT
- [ ] Configure baseline firewall policies
- [ ] Test outbound path from each segment
- [ ] Document firewall rule baseline
- [ ] Document traffic flow for each zone pair

## Topics

- Firewall zones and policies
- NAT (outbound/masquerade)
- Routing between CE and firewall
- Network segmentation
- North-south and east-west traffic control

## Risks / Blockers

- Phase 1 must be complete (routing to CE1 must work)
- Firewall platform choice (pfSense vs OPNsense) should be confirmed early

## Validation

- DMZ, SERVER, and CLIENT are separated and cannot reach each other without firewall policy
- Outbound path works from all internal segments
- Firewall logs show expected allow/deny behaviour

## Notes

- Define the firewall rule baseline before adding services
- Document the intended traffic matrix (who can reach what) before testing
- East-west policy should default to deny and be opened deliberately

## Exit Criteria

- DMZ, SERVER, and CLIENT segments are separated
- Firewall controls are tested and behave as documented
- Path from client to outside is fully documented
