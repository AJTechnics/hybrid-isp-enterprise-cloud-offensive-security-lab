# Naming Standards

## Hostname Convention

Hostnames follow a `<role><index>` pattern. Names are short, lowercase, and reflect function — not personal labels.

## Device Hostnames

| Hostname | Role |
|---|---|
| isp-core1 | Provider core router 1 |
| isp-core2 | Provider core router 2 |
| isp-edge1 | Simulated transit/edge router |
| pe1 | Provider edge router |
| ce1 | Customer edge router |
| fw1 | Enterprise firewall |
| win-ad1 | Windows Server — AD and DNS |
| app1 | Linux application server |
| lb1 | Load balancer (HAProxy) |
| kali1 | Kali Linux offensive host |
| vuln1 | Vulnerable target host |
| netbox1 | NetBox SoT instance |
| auto1 | Automation node (Ansible) |
| mon1 | Monitoring node |

## Naming Principles

- Keep names short and obvious
- One role per VM where possible
- Reflect function, not personal labels
- Use index suffix (1, 2) for redundant devices
- Prefix with domain shorthand for clarity (`isp-`, `win-`)

## Interface Naming

- Use descriptive names where platform allows: `eth0`, `eth1`, etc.
- Document interface-to-segment mapping in the inventory
- Use loopback interface for router IDs and BGP source

## VLAN Naming

| VLAN Name | Segment |
|---|---|
| MGMT | Management |
| DMZ | Demilitarized zone |
| SERVER | Server segment |
| CLIENT | Client/user segment |
| SECURITY | Offensive/attacker segment |
| AUTOMATION | NetBox and tooling |

## DNS Naming

- Domain: `lab.local` (or equivalent internal domain — TBD)
- Pattern: `<hostname>.lab.local`
- Example: `win-ad1.lab.local`, `app1.lab.local`
