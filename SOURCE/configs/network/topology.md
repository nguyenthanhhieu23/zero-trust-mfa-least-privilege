# Sơ đồ mạng Zero Trust LAN

Sơ đồ dưới đây dùng cho lab Docker hoặc có thể ánh xạ sang EVE-NG, PNETLab, VMware, VirtualBox hay Hyper-V.

```mermaid
flowchart LR
    Internet((Internet / Attacker)) --> FW[Edge Firewall\nDefault deny\nNAT + logging]
    FW --> DMZ[DMZ - VLAN 50\n172.16.50.0/24]
    FW --> CORE[Core L3 Switch / Router\nInter-VLAN policy]

    subgraph DMZ
        KC[Keycloak\nOIDC + MFA\n172.16.50.10]
        GW[Reverse Proxy /\nDemo Application\n172.16.50.20]
    end

    subgraph TRUSTED[Internal VLANs - no implicit trust]
        USERS[User VLAN 10\n172.16.10.0/24\nuser-client]
        SERVERS[Server VLAN 20\n172.16.20.0/24\nfile/API server]
        ADMINS[Admin VLAN 30\n172.16.30.0/24\nadmin-client]
        GUESTS[Guest VLAN 40\n172.16.40.0/24\nguest-client]
        MGMT[Management VLAN 60\n172.16.60.0/24\nmonitoring/logs]
    end

    CORE --> USERS
    CORE --> SERVERS
    CORE --> ADMINS
    CORE --> GUESTS
    CORE --> MGMT

    USERS -. "1. OIDC login + MFA" .-> KC
    ADMINS -. "1. OIDC login + MFA" .-> KC
    GUESTS -. "1. OIDC login + MFA" .-> KC
    KC -. "2. token with role" .-> GW
    USERS -->|role=user: approved API only| GW
    ADMINS -->|role=admin: approved admin API| GW
    GUESTS -->|role=guest: public/read-only only| GW
    GW -->|service account / allowlist| SERVERS
    MGMT -->|logs and monitoring only| FW

    FW -. "deny by default + audit" .-> SERVERS
    FW -. "deny guest-to-internal" .-> GUESTS
```

## Bảng phân vùng và quyền

| VLAN | Mạng | Thành phần | Quyền chính |
|---|---|---|---|
| 10 | `172.16.10.0/24` | Máy người dùng | Đăng nhập MFA; chỉ gọi API được cấp |
| 20 | `172.16.20.0/24` | File/API server | Chỉ nhận kết nối từ gateway hoặc luồng được allowlist |
| 30 | `172.16.30.0/24` | Máy quản trị | MFA bắt buộc; truy cập quản trị theo role và nguồn |
| 40 | `172.16.40.0/24` | Máy khách/khách | Chỉ Internet và dịch vụ công khai; cấm truy cập nội bộ |
| 50 | `172.16.50.0/24` | Keycloak, reverse proxy | DMZ; không truy cập tùy ý vào server nội bộ |
| 60 | `172.16.60.0/24` | Log/monitoring | Chỉ nhận log và thực hiện giám sát quản trị |

## Luồng demo bắt buộc

1. **Lab setup:** dựng firewall, các VLAN/network, Keycloak, gateway và server; tạo `admin`, `user`, `guest`.
2. **Exploitation/test:** thử truy cập server trực tiếp, thử bỏ qua MFA, thử dùng token sai role, và thử `guest` truy cập vùng nội bộ.
3. **Defense & mitigation:** bật default-deny, bắt buộc MFA, kiểm tra role trong gateway, giới hạn source/destination và ghi log.
4. **Re-test:** chạy lại đúng các lệnh kiểm thử; truy cập hợp lệ phải thành công, truy cập sai role hoặc sai VLAN phải bị từ chối và có log.

## Nguyên tắc an toàn

Chỉ thực hiện kiểm thử trên lab cô lập, dùng tài khoản và dữ liệu giả. Không quét hoặc khai thác mạng doanh nghiệp thật khi chưa có ủy quyền bằng văn bản.