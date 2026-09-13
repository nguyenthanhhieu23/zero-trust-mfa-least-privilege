# Firewall lab

`firewall-rules.sh` is a Linux host example using nftables. Run it only on an
isolated lab host with root privileges. The script is intentionally not applied
by Docker Compose because Docker and the host firewall have different network
namespaces.