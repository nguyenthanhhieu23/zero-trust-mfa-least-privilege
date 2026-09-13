#!/usr/bin/env bash
set -euo pipefail

sudo nft -f - <<'NFT'
flush ruleset

table inet zero_trust {
  chain forward {
    type filter hook forward priority 0; policy drop;
    ct state established,related accept

    # Keycloak and the demo gateway are reachable from lab clients.
    ip daddr 172.16.50.10 tcp dport 8080 accept
    ip daddr 172.16.50.20 tcp dport 5000 accept

    # Only the gateway may reach the protected server network.
    ip saddr 172.16.50.20 ip daddr 172.16.20.0/24 tcp dport 443 accept

    # Management traffic is restricted to the management VLAN.
    ip saddr 172.16.60.0/24 ip daddr 172.16.20.0/24 tcp dport 22 accept
    log prefix "zero-trust-deny " flags all counter drop
  }
}
NFT