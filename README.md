# SDN-BASED DYNAMIC FIREWALL FOR SCHOOL NETWORKS
**(Phiên bản: Shannon Entropy & Lightweight Automation)**

## 1. Tổng quan
Dự án xây dựng một hệ thống **Tường lửa động (Dynamic Firewall)** dành cho mạng nội bộ trường học (ví dụ: Phòng thực hành, Thư viện), tập trung vào việc giải quyết **"Mối đe dọa nội bộ" (Insider Threats)**.

Khác với các giải pháp SDN truyền thống sử dụng Controller cồng kềnh (như Ryu/ONOS), dự án này tiếp cận theo hướng **Lightweight Automation** (Tự động hóa hạng nhẹ):
- Sử dụng **Python Script** để tương tác trực tiếp với **Open vSwitch (OVS)**.
- Tích hợp thuật toán **Shannon Entropy** để phát hiện tấn công DDoS/Flood dựa trên tính ngẫu nhiên của gói tin thay vì chỉ đếm số lượng đơn thuần.
- Tích hợp **Captive Portal** để mô phỏng quy trình xác thực người dùng.

> **Mục tiêu:** Phát hiện và ngăn chặn tức thời các máy trạm (Host) bị nhiễm mã độc hoặc sinh viên cố tình thực hiện tấn công DoS trong mạng LAN, đảm bảo kết nối ổn định cho các máy khác.

---

## 2. Tính năng nổi bật

### 2.1 Phát hiện tấn công bằng Shannon Entropy (AI)
Thay vì sử dụng ngưỡng tĩnh (Static Threshold) dễ bị qua mặt, hệ thống phân tích độ hỗn loạn thông tin (Entropy) của lưu lượng mạng:
- **Traffic sạch (Normal):** Entropy cao do tính ngẫu nhiên của hành vi lướt web/truy cập đa dạng.
- **Traffic tấn công (Attack):** Entropy giảm đột ngột (tiệm cận 0.0) do các công cụ tấn công thường gửi gói tin lặp lại (cố định IP đích, port, sequence number...) để tối ưu hiệu suất.

### 2.2 Cơ chế phản ứng thời gian thực
- Ngay khi phát hiện Entropy giảm dưới mức an toàn, hệ thống tự động gọi lệnh hệ thống (CLI Wrapping) để đẩy luật `DROP` vào bảng dòng (Flow Table) của Switch.
- Thời gian phản ứng < 1 giây.

### 2.3 Mô phỏng xác thực (Captive Portal)
- Giao diện Web (Flask) mô phỏng cổng đăng nhập Wifi/LAN của trường học.
- Giúp định danh người dùng trước khi truy cập mạng.

---
