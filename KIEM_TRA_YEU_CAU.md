# Kiểm tra yêu cầu đề tài

## Đánh giá hiện trạng

Workspace ban đầu chưa có file triển khai. Cấu trúc trong đề bài là phù hợp về mặt tổ chức, nhưng để được xem là hoàn chỉnh cần bổ sung nội dung cho từng phần và bằng chứng chạy lab.

## Đối chiếu 4 phần bắt buộc

| Phần | Nội dung cần có | Trạng thái cần hoàn thiện |
|---|---|---|
| 1. Lý thuyết | Zero Trust, MFA, Least Privilege, VLAN, firewall, Keycloak/OIDC, các rủi ro và biện pháp giảm thiểu | Cần viết trong báo cáo |
| 2. Mô hình triển khai | Sơ đồ mạng, địa chỉ IP/VLAN, vai trò các máy, cách dựng bằng Docker hoặc máy ảo | Đã tạo sơ đồ mẫu trong `SOURCE/configs/network/topology.md` |
| 3. Kịch bản demo | Setup, kiểm thử/tấn công trong lab, phòng thủ/giám sát, kiểm tra lại sau phòng thủ | Cần chạy và lưu log/kết quả trước-sau |
| 4. Kết luận | Tính khả thi, giới hạn, chi phí, bài học áp dụng cho doanh nghiệp | Cần hoàn thiện trong báo cáo |

## Các bằng chứng nên có trong bài nộp

- Ảnh hoặc file cấu hình topology và địa chỉ IP/VLAN.
- Log đăng nhập Keycloak có MFA thành công và thất bại.
- Kết quả kiểm thử trước khi bật chính sách: truy cập trái phép còn xảy ra.
- Kết quả kiểm thử sau khi bật chính sách: truy cập bị chặn theo VLAN, role và MFA.
- Bảng quyền của `admin`, `user`, `guest`, kèm các lệnh kiểm tra tương ứng.
- Log firewall và thời điểm thực hiện từng bước demo.

## Điều kiện để kết luận đạt

Đề tài đạt yêu cầu khi nhóm chứng minh được: người dùng phải xác thực MFA, mỗi role chỉ truy cập đúng tài nguyên được cấp, lưu lượng không được cấp phép bị từ chối mặc định, và kết quả sau phòng thủ được đo lại bằng cùng một bộ kiểm thử như trước phòng thủ.