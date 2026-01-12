import subprocess
import requests
import time
import re
import os
import sys

# --- CẤU HÌNH ---
# Địa chỉ API của Firewall (Bộ não)
FIREWALL_API = "http://127.0.0.1:9000/firewall/event"

# Ngưỡng cảnh báo: Nếu 1 IP gửi > 200 gói tin trong thời gian ngắn -> Báo động
THRESHOLD_PACKETS = 200 

# Switch cần giám sát (trong Mininet thường là s1)
SWITCH_NAME = "s1"

print(f"[IDS] 🛡️  Starting Watcher on {SWITCH_NAME}...")

# 1. Kiểm tra quyền ROOT (Tránh lỗi hỏi mật khẩu giữa chừng)
if os.geteuid() != 0:
    print("[ERROR] Script này cần quyền Root để đọc dữ liệu Switch!")
    print("👉 Hãy chạy lại bằng lệnh: sudo python3 ids_watcher.py")
    sys.exit(1)

def get_flows():
    """Đọc dữ liệu luồng từ Open vSwitch"""
    try:
        # Lệnh này tương đương gõ 'sudo ovs-ofctl dump-flows s1'
        result = subprocess.run(
            ["ovs-ofctl", "dump-flows", SWITCH_NAME],
            capture_output=True, text=True
        )
        return result.stdout
    except Exception as e:
        print(f"[ERROR] Không thể đọc OVS: {e}")
        return ""

def parse_and_detect(raw_data):
    """Phân tích log để tìm IP đang spam gói tin"""
    
    # Regex tìm dòng có IP nguồn (nw_src) và số lượng gói tin (n_packets)
    # Mẫu log OVS: ... tcp,nw_src=10.0.0.1,tp_dst=80 ... n_packets=5000 ...
    pattern = re.compile(r"nw_src=([\d\.]+),.*n_packets=(\d+)")
    
    suspicious_ips = []
    
    for line in raw_data.split("\n"):
        # Chỉ quan tâm các dòng có giao thức IP (bỏ qua ARP, IPv6 nếu không cần)
        if "nw_src" in line:
            match = pattern.search(line)
            if match:
                ip_src = match.group(1)
                packets = int(match.group(2))
                
                # LOGIC PHÁT HIỆN TẤN CÔNG ĐƠN GIẢN
                # Nếu số gói tin vượt ngưỡng -> Nghi ngờ Flood
                if packets > THRESHOLD_PACKETS:
                    # Bỏ qua các IP nội bộ an toàn (như Gateway 10.0.0.254) nếu cần
                    if ip_src == "10.0.0.254": 
                        continue
                        
                    suspicious_ips.append((ip_src, packets))
    
    return suspicious_ips

# --- VÒNG LẶP CHÍNH ---
while True:
    flows = get_flows()
    alerts = parse_and_detect(flows)

    for ip, packet_count in alerts:
        print(f"[IDS] 🚨 ALERT! Phát hiện High Traffic từ {ip} ({packet_count} packets)")
        
        # Tạo bản tin gửi cho AI
        payload = {
            "src_ip": ip,
            "packet_count": packet_count,  # AI cần cái này để tính Score
            "reason": "Syn Flood/High Traffic Detected",
            "confidence": 0.99
        }
        
        try:
            # Gửi cảnh báo sang Firewall API
            response = requests.post(FIREWALL_API, json=payload, timeout=1)
            if response.status_code == 200:
                print(f"[IDS] ✅ Đã gửi báo cáo về {ip} cho AI xử lý.")
            else:
                print(f"[IDS] ⚠️ AI phản hồi lỗi: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("[IDS] ❌ Không thể kết nối tới Firewall API (Server có đang chạy không?)")
        except Exception as e:
            print(f"[IDS] Lỗi gửi request: {e}")

    # Quét lại sau mỗi 2 giây
    time.sleep(2)
