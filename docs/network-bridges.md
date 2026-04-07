# Proxmox Network Bridges

## Current bridge usage

### vmbr0
- management bridge
- connected to the active LAN uplink
- used for:
  - Proxmox UI
  - SSH
  - workspace VM access

### vmbr1
- reserved for PE ↔ CE path

### vmbr2
- isp-core1 ↔ isp-core2

### vmbr3
- isp-core1 ↔ pe1

### vmbr4
- isp-core2 ↔ pe1

### vmbr5
- isp-core1 ↔ isp-edge1

## Notes

- current physical uplink path uses the UniFi switch
- MikroTik integration is planned later
- lab bridges are internal topology links and should not carry management IPs
