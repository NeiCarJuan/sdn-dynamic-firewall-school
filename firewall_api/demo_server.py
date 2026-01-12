import sys
import os
import subprocess
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
BLOCKED_IPS = []

def force_block_ip(ip_address):
    print(f"   [EXECUTING] Applying DROP rule for {ip_address} on Switch s1...")
    try:
        # Thêm cờ -O OpenFlow13 để tương thích với Switch OVS
        # Dùng subprocess để không bị treo nếu lỗi
        cmd = f"ovs-ofctl -O OpenFlow13 add-flow s1 priority=50000,dl_type=0x0800,nw_src={ip_address},actions=drop"
        
        # Chạy lệnh (Vì server đã chạy sudo nên không cần sudo ở đây nữa)
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        
        print("   ✅ [SUCCESS] RULE APPLIED! Traffic should stop immediately.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ [ERROR] Command failed: {e.output.decode().strip()}")
        return False

@app.route('/')
def home(): return "<h1>🛡️ HUST FIREWALL ACTIVE</h1>"

@app.route('/login', methods=['POST'])
def login(): return jsonify({"status": "success"})

@app.route("/firewall/event", methods=["POST"])
def handle_event():
    data = request.json
    src_ip = data.get("src_ip")
    try: packet_count = int(data.get("packet_count", 0))
    except: packet_count = 0

    if src_ip == "10.0.0.2": return jsonify({"status": "ignored"})

    # Logic chặn (>1000 là chặn ngay)
    if packet_count > 1000:
        # Luôn gọi lệnh chặn để đảm bảo (kể cả đã chặn rồi)
        force_block_ip(src_ip)
        if src_ip not in BLOCKED_IPS:
            BLOCKED_IPS.append(src_ip)
            print(f"🔥 [AI ALERT] BLOCKING {src_ip} NOW!")
            
    return jsonify({"status": "processed"})

if __name__ == "__main__":
    # Kiểm tra quyền Root
    if os.geteuid() != 0:
        print("❌ ERROR: Please run with SUDO (sudo python3 ...)")
        sys.exit(1)
        
    print(">>> 🚀 ROOT SERVER READY on port 5000")
    app.run(host='0.0.0.0', port=5000)
