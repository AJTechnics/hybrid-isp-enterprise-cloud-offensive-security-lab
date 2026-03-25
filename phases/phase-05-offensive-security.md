# Phase 05 — Offensive Security Segment

## Goal

Test the environment from an attacker point of view. Validate segmentation assumptions and document findings.

## Scope

SECURITY segment: kali1, vuln1, and controlled attack paths against existing lab services.

## Components

- kali1 — Kali Linux offensive host
- vuln1 — intentionally vulnerable host (DVWA / Metasploitable)
- Optional: expose a lab web app as a target

## Tasks

- [ ] Deploy kali1
- [ ] Deploy vuln1 (DVWA or Metasploitable)
- [ ] Configure firewall to isolate SECURITY segment appropriately
- [ ] Run recon from kali1 against lab environment
- [ ] Document what is visible from the attacker segment
- [ ] Run enumeration against accessible services
- [ ] Test HTTP/application inspection against web targets
- [ ] Validate firewall and segmentation assumptions
- [ ] Document hardening observations
- [ ] List defensive improvements based on findings

## Topics

- Recon and OSINT within lab scope
- Service enumeration
- HTTP inspection and web application testing
- Segmentation validation
- Firewall exposure analysis
- Defensive hardening based on offensive findings

## Risks / Blockers

- This segment should be isolated from MGMT and AUTOMATION at the firewall
- vuln1 must not be reachable from outside the lab environment
- Document scope clearly — only attack intended targets

## Validation

- Attacker-to-target path is understood and documented
- Findings are written up clearly with evidence
- Defensive improvements are listed with priority

## Notes

- Treat this like a scoped penetration test against your own lab
- Keep findings professional — write them as you would in a real report
- Firewall rule review is part of the validation

## Exit Criteria

- Attacker-to-target path is understood
- Findings are documented clearly
- Defensive improvements are listed
