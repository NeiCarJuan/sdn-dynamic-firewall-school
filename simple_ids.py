import time
import requests
from collections import defaultdict
from scapy.all import sniff, IP

API_URL = "http://127.0.0.1:5000/firewall/event"
INTERVAL = 1.0
THRESHOLD_REPORT = 50 

# --- [QUAN TRỌNG] TÊN CARD MẠNG MININET ---
# s1-eth1 là cổng nối với h1 (Alice). 
# Nếu báo lỗi "No such device", hãy thử đổi thành "s1" hoặc chạy lệnh "ip a" để xem tên.
LISTEN_INTERFACE = "s1-eth1" 

print(f"👀 IDS SENSOR STARTED on {LISTEN_INTERFACE}...")

packet_counts = defaultdict(int)

def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        if src_ip.startswith("10.0.0."):
            packet_counts[src_ip] += 1

def start_monitoring():
    while True:
        try:
            # Nghe trên interface cụ thể của Mininet
            sniff(iface=LISTEN_INTERFACE, filter="ip", prn=packet_callback, timeout=INTERVAL, store=0)
        except OSError:
            print(f"❌ ERROR: Interface {LISTEN_INTERFACE} not found! Check Mininet is running.")
            return

        for ip, count in list(packet_counts.items()):
            pps = count / INTERVAL
            if pps > THRESHOLD_REPORT:
                print(f"📡 DETECTED: {ip} sending {int(pps)} packets/sec -> REPORTING...")
                try:
                    payload = {"src_ip": ip, "packet_count": int(pps)}
                    requests.post(API_URL, json=payload, timeout=0.1)
                except: pass
            packet_counts[ip] = 0

if __name__ == "__main__":
    start_monitoring()
