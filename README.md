- Controller đã được chuyển từ **Ryu → Faucet**
- Thư mục `legacy-ryu/` lưu phiên bản cũ để tham khảo
- Hệ thống hiện tại sử dụng **Faucet + ACL** để triển khai SDN Firewall
# Tường lửa động dựa trên SDN cho mạng trường học


## 1. Tổng quan
Dự án xây dựng một **hệ thống tường lửa động dựa trên SDN** nhằm bảo vệ **mạng khuôn viên trường học**, sử dụng:
- **OpenFlow + Ryu Controller** (mặt phẳng điều khiển)
- **Mininet + Open vSwitch** (mặt phẳng dữ liệu – mô phỏng)
- **Mô-đun AI đơn giản dựa trên thống kê (z-score)** để phát hiện bất thường
- **Cơ chế học thích nghi (auto-learn)**: sau khi phát hiện tấn công mới, controller ghi nhớ mẫu và nâng cấp thành rule “đã biết”
- **Captive Portal + Dashboard (Flask)** để xác thực người dùng và hiển thị trạng thái/log

> Mục tiêu: bảo vệ các dịch vụ mạng trường học (LMS / website / dịch vụ nội bộ) trước các hình thức tấn công phổ biến như DoS/flooding, scan, đồng thời liên kết hành vi traffic với danh tính người dùng đã xác thực.

---

## 2. Các tính năng chính

### 2.1 Phòng thủ hai lớp
- **Tấn công đã biết**: được phát hiện bằng các rule tĩnh định nghĩa sẵn (drop / limit ngay tại switch).
- **Tấn công chưa biết**: được phát hiện bởi AI (z-score) → controller sinh rule động để giảm thiểu.

### 2.2 Cơ chế học thích nghi (Auto-learn)
Khi phát hiện một tấn công mới:
1. AI đánh dấu traffic là bất thường
2. Controller áp dụng rule phòng thủ động
3. Controller lưu mẫu tấn công vào bộ nhớ “learned signatures”
4. Nếu mẫu lặp lại vượt ngưỡng, nó được **nâng cấp thành rule tĩnh (tấn công đã biết)**

Cơ chế này giúp hệ thống phản ứng nhanh hơn với các tấn công lặp lại trong tương lai.

---

### 2.3 Captive Portal & Gắn danh tính người dùng
- Người dùng phải **đăng nhập qua Captive Portal** trước khi được cấp quyền truy cập đầy đủ.
- Dashboard hiển thị:
  - các host đã xác thực
  - log tấn công / cảnh báo
  - các mẫu tấn công đã học
  - (tuỳ chọn) các rule firewall đang hoạt động

---

## 3. Kiến trúc hệ thống (tổng quan)

### Mặt phẳng dữ liệu (Data Plane)
- Các host (sinh viên / giảng viên / khách) kết nối tới switch OpenFlow (OVS).
- Các dịch vụ: server trường học (LMS / Web), Internet (tuỳ chọn trong mô phỏng).

### Mặt phẳng điều khiển (Control Plane)
- Ryu Controller cài đặt FlowMod, thu thập thống kê, phát hiện bất thường và thực hiện phòng thủ.

### Mặt phẳng quản lý (Management Plane)
- Captive Portal & Dashboard (Flask) giao tiếp với controller thông qua REST API.

---

## 4. Cấu trúc thư mục dự án

- `controller/`: Controller SDN, firewall, AI, topology Mininet, REST API (chạy trên Ubuntu VM).
- `portal/`: Captive Portal và Dashboard (Flask Web App).
- `docs/`: báo cáo, sơ đồ, slide, kịch bản demo.
- `scripts/`: script hỗ trợ khởi động, reset, demo.

---

## 5. Phân công nhóm

- **Ninh**: SDN Controller (Ryu), firewall rule (tĩnh & động), AI z-score, cơ chế học, mô phỏng Mininet, kịch bản tấn công.
- **Biên**: Captive Portal, Dashboard, giao diện web, tích hợp REST API, hình ảnh/UI cho báo cáo và demo.

---

## 6. Yêu cầu môi trường (tóm tắt)

### 6.1 Ninh (Ubuntu VM)
- Ubuntu 22.04 LTS (khuyến nghị)
- Python 3.10+
- Ryu Controller
- Mininet + Open vSwitch
- Công cụ hỗ trợ: `iperf3`, `hping3`, `nmap`

### 6.2 Biên (Windows hoặc hệ điều hành bất kỳ)
- Python 3.10+
- Flask
- Thư viện `requests`
- Trình duyệt web

---

## 7. REST API (hợp đồng tối thiểu)

### Portal → Controller
- `POST /api/login`  
  Dữ liệu:
  ```json
  {
    "mac": "...",
    "ip": "...",
    "username": "...",
    "role": "student | teacher | guest"
  }
