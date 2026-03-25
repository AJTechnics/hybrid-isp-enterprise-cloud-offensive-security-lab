# Services

Document lab services and their endpoints here.

## Service Registry

| Service | Host | Protocol | Port | VIP / Endpoint | Segment | Phase | Status |
|---|---|---|---|---|---|---|---|
| Active Directory | win-ad1 | LDAP/Kerberos | 389/88 | TBD | SERVER | 3 | planned |
| DNS | win-ad1 | UDP/TCP | 53 | TBD | SERVER | 3 | planned |
| Web App (backend) | app1 | HTTP | 80 | TBD | SERVER | 3 | planned |
| Load Balancer VIP | lb1 | HTTP/HTTPS | 80/443 | TBD | DMZ | 4 | planned |
| NetBox | netbox1 | HTTPS | 443 | TBD | AUTOMATION | 6 | planned |
| Ansible | auto1 | SSH | 22 | TBD | AUTOMATION | 6 | planned |
| Monitoring | mon1 | HTTPS | 443 | TBD | AUTOMATION | 7 | planned |
| DVWA / vuln app | vuln1 | HTTP | 80 | TBD | SECURITY | 5 | planned |

## Notes

- Update endpoints and status as services are deployed
- Document firewall rules that allow each service
- Cross-reference with ip-plan.md for address assignments
