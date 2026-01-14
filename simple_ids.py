import time
import requests
import logging
from collections import defaultdict
from scapy.all import sniff, IP

# --- CẤU HÌNH KẾT NỐI SERVER ---
API_URL = "http://127.0.0.1:5000/firewall/event"
INTERVAL = 1.0          # Chu kỳ gửi báo cáo (1 giây/lần)
MIN_PACKETS_TO_SEND = 5 # Chỉ gửi nếu bắt được ít nhất 5 gói tin (để tránh rác)

# --- [QUAN TRỌNG] TÊN CARD MẠNG MININET ---
# Nếu bạn nối h1 vào cổng 1 của s1, tên thường là "s1-eth1"
# Kiểm tra bằng lệnh: ip link show (trên máy thật khi Mininet đang chạy)
LISTEN_INTERFACE = "s1-eth1"

print(f"👀 IDS SENSOR STARTED on interface [{LISTEN_INTERFACE}]...")
print(f"   -> Mode: Entropy Data Collection")
print(f"   -> Reporting to: {API_URL}")

# Biến lưu trữ tạm thời trong 1 chu kỳ
src_packet_counts = defaultdict(int) # Đếm số lượng gửi của mỗi IP nguồn (để tìm nghi phạm)
dest_ip_samples = []                 # Danh sách các IP đích (để tính Entropy)

def packet_callback(packet):
    """Hàm này được gọi mỗi khi bắt được 1 gói tin"""
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # Chỉ theo dõi traffic nội bộ 10.0.0.x để giảm nhiễu
        if src_ip.startswith("10.0.0."):
            # 1. Lưu IP đích để Server tính Entropy (Độ tập trung)
            dest_ip_samples.append(dst_ip)

            # 2. Đếm số lượng gói từ nguồn này (Để biết ai là thủ phạm nếu có DDoS)
            src_packet_counts[src_ip] += 1

def start_monitoring():
    global src_packet_counts, dest_ip_samples

    while True:
        try:
            # Bắt gói tin trong khoảng thời gian INTERVAL (ví dụ 1 giây)
            # store=0 để không lưu vào RAM tránh tràn bộ nhớ
            sniff(iface=LISTEN_INTERFACE, filter="ip", prn=packet_callback, timeout=INTERVAL, store=0)
        except OSError:
            print(f"❌ ERROR: Interface '{LISTEN_INTERFACE}' not found!")
            print("   -> Tip: Open another terminal and run 'ip link' to check correct name.")
            return
        except Exception as e:
            print(f"❌ ERROR: Scapy error: {e}")
            return

        # --- XỬ LÝ DỮ LIỆU SAU MỖI 1 GIÂY ---
        total_packets = len(dest_ip_samples)

        if total_packets > MIN_PACKETS_TO_SEND:
            # Tìm ra "Nghi phạm" (IP gửi nhiều nhất trong giây vừa rồi)
            # Logic: Lấy key (IP) có value (count) lớn nhất
            if src_packet_counts:
                suspect_ip = max(src_packet_counts, key=src_packet_counts.get)
                packet_rate = src_packet_counts[suspect_ip]
            else:
                suspect_ip = "Unknown"
                packet_rate = 0

            print(f"📡 SENDING SAMPLE: {total_packets} pkts captured | Top Source: {suspect_ip} ({packet_rate} pps)")

            # Đóng gói dữ liệu gửi cho AI Server
            payload = {
                "dest_ips": dest_ip_samples, # Dữ liệu quan trọng nhất cho Entropy
                "src_ip": suspect_ip,        # Kẻ bị tình nghi
                "packet_count": packet_rate  # Thông tin phụ
            }

            try:
                # Gửi Request POST (timeout ngắn để không làm treo IDS)
                requests.post(API_URL, json=payload, timeout=0.1)
            except requests.exceptions.RequestException:
                print(f"⚠️ Warning: Could not connect to Firewall Server at {API_URL}")

        # --- RESET BỘ ĐẾM CHO CHU KỲ MỚI ---
        src_packet_counts.clear()
        dest_ip_samples.clear()

if __name__ == "__main__":
    # Yêu cầu quyền Root để chạy Scapy sniff
    import os
    if os.geteuid() != 0:
        print("❌ ERROR: Please run this script with SUDO!")
        exit(1)

    start_monitoring()
