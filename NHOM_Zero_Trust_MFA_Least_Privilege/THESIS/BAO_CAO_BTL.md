# Triển khai kiến trúc Zero Trust cho mạng LAN doanh nghiệp

## 1. Mở đầu

Trong môi trường mạng doanh nghiệp hiện đại, các mô hình bảo mật truyền thống dựa trên ranh giới mạng đã không còn đủ để đối phó với các mối đe dọa từ bên trong và từ xa. Vì vậy, mô hình Zero Trust ra đời với nguyên tắc: không tin tưởng bất kỳ đối tượng nào, kể cả người dùng trong mạng nội bộ, và luôn yêu cầu xác thực, ủy quyền và giám sát liên tục.

Đề tài này triển khai một môi trường lab mô phỏng Zero Trust bằng cách kết hợp:
- Keycloak làm Identity Provider (IdP)
- OpenID Connect (OIDC) và JWT để xác thực và ủy quyền
- MFA/TOTP để tăng mức độ xác thực
- Least Privilege để giới hạn quyền truy cập theo vai trò
- Docker để dựng môi trường lab nhanh, dễ tái tạo

## 2. Mục tiêu đề tài

- Xây dựng mô hình Zero Trust trong môi trường lab nội bộ.
- Sử dụng MFA/TOTP để tăng độ tin cậy cho xác thực người dùng.
- Phân quyền theo vai trò `admin`, `user`, `guest`.
- Kiểm chứng rằng người dùng chỉ truy cập được tài nguyên được phép.
- So sánh trước và sau khi áp dụng chính sách Zero Trust.

## 3. Cơ sở lý thuyết

### 3.1 Zero Trust
Zero Trust là mô hình bảo mật theo nguyên tắc “không tin tưởng và luôn kiểm tra”. Các yêu cầu cốt lõi gồm:
- Xác thực từng request
- Ủy quyền theo vai trò và ngữ cảnh
- Phân đoạn mạng và truy cập tối thiểu
- Giám sát, nhật ký và cảnh báo liên tục

### 3.2 MFA
MFA yêu cầu người dùng xác thực qua ít nhất hai yếu tố khác nhau, ví dụ:
- Thông tin biết: mật khẩu
- Thông tin sở hữu: TOTP từ ứng dụng xác thực

Điều này làm giảm nguy cơ tài khoản bị đánh cắp hoặc lạm dụng.

### 3.3 Least Privilege
Least Privilege là nguyên tắc cấp quyền tối thiểu cần thiết cho nhiệm vụ cụ thể. Người dùng guest không được phép truy cập vào endpoint quản trị; user chỉ được truy cập dữ liệu người dùng; admin mới được truy cập dữ liệu quản trị.

### 3.4 Keycloak, OIDC và JWT
Keycloak là giải pháp IAM phổ biến hỗ trợ:
- Quản lý người dùng
- Quản lý role và realm
- MFA/TOTP
- OIDC và OAuth2

OIDC sử dụng JWT để trao đổi thông tin nhận dạng. Flask API trong lab sẽ xác thực JWT bằng cách:
- kiểm tra issuer
- kiểm tra audience
- kiểm tra chữ ký bằng JWKS
- đọc `realm_access.roles`

## 4. Mô hình triển khai

### 4.1 Kiến trúc lab
Môi trường lab được dựng bằng Docker Compose với 2 service chính:
- `keycloak`: chạy Keycloak 25.0
- `demo-app`: chạy Flask API validator

### 4.2 Kiến trúc mạng logic
- `dmz`: thông tin liên lạc giữa Keycloak và ứng dụng
- `servers`: mạng nội bộ cho ứng dụng backend

### 4.3 Vai trò trong hệ thống
| Vai trò | Mô tả | Quyền truy cập |
|---|---|---|
| admin | Quản trị hệ thống | /api/public, /api/admin |
| user | Người dùng nghiệp vụ | /api/public, /api/user |
| guest | Khách truy cập giới hạn | /api/public |

### 4.4 Cấu hình môi trường
Các file cấu hình chính:
- [SETUP/docker-compose.yml](../SETUP/docker-compose.yml)
- [SETUP/.env.example](../SETUP/.env.example)
- [SOURCE/app/app.py](../SOURCE/app/app.py)
- [SOURCE/configs/keycloak/users.txt](../SOURCE/configs/keycloak/users.txt)

## 5. Kịch bản demo

### Bước 1: Thiết lập môi trường
- Chạy Docker Compose
- Khởi động Keycloak
- Khởi động Flask API

Lệnh kiểm tra:

```bash
cd SETUP
Copy-Item .env.example .env
docker compose --env-file .env up -d --build
```

### Bước 2: Kiểm tra trạng thái hệ thống
- `/health` của API phải trả về status ok
- OIDC discovery phải trả về JSON có `issuer`, `authorization_endpoint`, `token_endpoint`

### Bước 3: Lấy token cho từng user
Script tạo token cho 3 tài khoản đã chạy thành công. Kết quả thực tế:
- admin: token thành công
- user: token thành công
- guest: token thành công

### Bước 4: Kiểm thử quyền truy cập
Các endpoint được kiểm thử:
- `/api/public`
- `/api/user`
- `/api/admin`

### Bước 5: Đánh giá hiện trạng
Kết quả kiểm thử thực tế:

| Role | /api/public | /api/user | /api/admin |
|---|---:|---:|---:|
| admin | 200 | 401 | 200 |
| user | 200 | 200 | 403 |
| guest | 200 | 403 | 403 |

Kết quả này cho thấy:
- endpoint công khai có thể truy cập công cộng
- user được quyền truy cập user-data nhưng không được truy cập admin-data
- guest bị chặn ở cả user và admin
- admin có quyền truy cập admin-data

## 6. Kết quả đạt được

- Môi trường Zero Trust lab đã được dựng và chạy ổn định.
- Keycloak tích hợp MFA/TOTP và role-based access control.
- JWT được xác thực với `issuer`, `audience` và `JWKS`.
- Mỗi vai trò có quyền truy cập đúng theo nguyên tắc least privilege.
- 401 và 403 đã xảy ra đúng nơi cần thiết, chứng minh bộ lọc quyền hoạt động.

## 7. Kết luận

Đề tài đã thành công trong việc triển khai một mô hình Zero Trust cơ bản trên môi trường lab nội bộ. Việc phân tách quyền theo role, sử dụng MFA/TOTP, xác thực JWT và kiểm soát truy cập theo vai trò cho thấy khả năng ứng dụng thực tế của mô hình Zero Trust trong môi trường doanh nghiệp nhỏ và trung bình.

Hạn chế lớn của mô hình lab này là môi trường còn đơn giản, chưa mô phỏng firewall/VLAN/ACL thực tế đầy đủ. Tuy nhiên, nó cho thấy rõ cách Zero Trust được triển khai ở tầng ứng dụng và xác thực, đồng thời là nền tảng để mở rộng lên mạng thực tế và lưu lượng theo policy.

## 8. Tài liệu tham khảo

1. NIST SP 800-207, Zero Trust Architecture.
2. Keycloak Documentation, OpenID Connect and OAuth2.
3. OWASP Top 10 API Security Risks.
4. RFC 7519 – JSON Web Token (JWT).
5. Microsoft Zero Trust model overview.

## 9. Phụ lục

- Cấu hình Docker Compose: [SETUP/docker-compose.yml](../SETUP/docker-compose.yml)
- Script khởi động: [SOURCE/scripts/setup.sh](../SOURCE/scripts/setup.sh)
- Script test kết nối: [SOURCE/scripts/test-connectivity.sh](../SOURCE/scripts/test-connectivity.sh)
- Script test quyền: [SOURCE/scripts/test-least-privilege.sh](../SOURCE/scripts/test-least-privilege.sh)
- Script lấy token: [SOURCE/scripts/get_tokens.py](../SOURCE/scripts/get_tokens.py)

---

Bản báo cáo này được tổng hợp dựa trên kết quả kiểm thử và chạy thực tế của dự án trong môi trường local.
