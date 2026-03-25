# Phase 07 — AWS Hybrid Extension

## Goal

Extend the enterprise into the cloud. Build a VPC and establish hybrid connectivity to the on-prem lab.

## Scope

AWS account: VPC, subnets, EC2, and hybrid connectivity back to the lab (VPN or equivalent).

## Components

- AWS account foundation
- VPC
- Public and private subnets
- EC2 instance(s)
- Site-to-site VPN or equivalent hybrid connectivity

## Tasks

- [ ] Set up AWS account with appropriate IAM boundaries
- [ ] Design VPC CIDR (10.100.0.0/16)
- [ ] Create public and private subnets
- [ ] Configure route tables and internet gateway
- [ ] Deploy EC2 instance in private subnet
- [ ] Configure security groups
- [ ] Establish VPN connectivity to on-prem lab
- [ ] Verify route exchange between on-prem and AWS
- [ ] Verify EC2 is reachable from on-prem via hybrid path
- [ ] Document traffic path comparison: on-prem vs cloud
- [ ] Map AWS constructs to on-prem equivalents

## Topics

- VPC design and subnet planning
- Cloud routing (route tables, internet gateway, VGW)
- Security groups vs firewall rules
- Site-to-site VPN configuration
- Hybrid path troubleshooting

## Risks / Blockers

- AWS costs — use free tier where possible, tear down when not in use
- VPN connectivity from lab requires a public IP or equivalent tunnel endpoint
- Phase 6 (automation) can be extended to cover AWS with Ansible/Terraform

## Validation

- AWS VPC is deployed per design
- At least one EC2 host is reachable via hybrid path
- Hybrid connectivity is documented
- Traffic path comparison (on-prem vs cloud) is written up

## Notes

- Consider using Terraform for AWS infrastructure as code (extends Phase 6 automation)
- Document costs and teardown procedures to avoid unexpected billing
- Map: Security Group ↔ Firewall Rule, Route Table ↔ Routing Table, VGW ↔ PE

## Exit Criteria

- Path to AWS is working or fully understood
- Enterprise-to-cloud design is documented
- Key AWS networking concepts are mapped to lab topology
