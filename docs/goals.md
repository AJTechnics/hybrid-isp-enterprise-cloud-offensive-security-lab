# Project Goals

## Primary Goals

- Refresh and deepen high-level network engineering skills
- Regain hands-on confidence in routing, switching, security, and troubleshooting
- Build practical exposure to cloud networking and load balancing
- Create a platform for offensive security practice
- Support a future study group with shared tasks and documentation
- Create a portfolio project documented in Obsidian and GitHub

## How These Goals Will Be Reached

The project goals will be reached through a code-first and phase-based engineering workflow.

### Delivery Method
- Build the lab in phases rather than as one large deployment
- Prefer repeatable builds over one-off manual work
- Document each implementation step in GitHub and supporting notes
- Use templates and reusable modules to reduce drift and speed up rebuilds

### Technical Delivery Model
- Provision infrastructure with OpenTofu
- Use Proxmox templates for repeatable VM deployment
- Configure systems and services through automation rather than manual clicking
- Validate changes through testing, troubleshooting, and phased rollout
- Evolve toward source-of-truth-driven infrastructure with inventory and topology tracking

### Working Style
- Use daily coding sessions to improve implementation speed and depth
- Treat networking tasks as code and automation problems where possible
- Use the lab as both a learning platform and a portfolio project

## Technical Goals by Domain

### Provider Networking
- Build and operate a simulated ISP core with OSPF
- Configure PE/CE routing handoff (eBGP or static)
- Understand route advertisement and default routing at provider/customer boundary

### Enterprise Infrastructure
- Build segmented enterprise with firewall, DMZ, server, and client zones
- Deploy Active Directory, DNS, and supporting services
- Configure and validate firewall policies for north-south and east-west traffic

### Load Balancing
- Deploy HAProxy with L4 and L7 frontends
- Validate health checks, TLS termination, and persistence
- Map HAProxy concepts to F5 terminology and design patterns

### Cloud (AWS)
- Build a VPC with proper subnet and routing design
- Establish hybrid connectivity to the on-prem environment
- Compare cloud networking constructs to on-prem equivalents

### Offensive Security
- Test the environment from an attacker perspective
- Validate segmentation and firewall assumptions
- Document findings and hardening improvements

### Automation and SoT
- Represent the full lab in NetBox (devices, interfaces, prefixes, VLANs)
- Create initial Ansible playbooks
- Drive at least one lab change through automation

### Monitoring
- Deploy basic availability monitoring for critical nodes
- Create service checks and dashboards
- Build an operational mindset for the lab environment
