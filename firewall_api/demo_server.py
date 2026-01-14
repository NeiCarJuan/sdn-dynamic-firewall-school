import sys
import os
import subprocess
import math
from collections import Counter
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
BLOCKED_IPS = []

# --- CẤU HÌNH ENTROPY (AI) ---
ENTROPY_THRESHOLD = 0.5  # Dưới mức này là DDoS

# --- HÀM TÍNH ENTROPY ---
def calculate_entropy(ip_list):
    if not ip_list: return 0
    counts = Counter(ip_list)
    total = len(ip_list)
    entropy = 0
    for count in counts.values():
        prob = count / total
        entropy -= prob * math.log(prob, 2)
    return entropy

# --- HÀM CHẶN CỨNG ---
def force_block_ip(ip_address):
    print(f"   [EXECUTING] Applying DROP rule for {ip_address} on Switch s1...")
    try:
        cmd = f"ovs-ofctl -O OpenFlow13 add-flow s1 priority=50000,dl_type=0x0800,nw_src={ip_address},actions=drop"
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        print(f"   ✅ [SUCCESS] RULE APPLIED! Traffic from {ip_address} is now blocked.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ [ERROR] Command failed: {e.output.decode().strip()}")
        return False

# --- GIAO DIỆN CAPTIVE PORTAL (ĐÃ KHÔI PHỤC LẠI NGUYÊN BẢN) ---
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HUST AI Firewall System</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding-top: 80px; background: #eceff1; }
            .login-card { background: white; padding: 40px; border-radius: 12px; display: inline-block; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 350px; }
            h2 { color: #b71c1c; margin-bottom: 25px; }
            input { margin: 10px 0; padding: 12px; width: 100%; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { padding: 12px; width: 100%; background: #b71c1c; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 15px; }
            button:hover { background: #d32f2f; }
            .status { margin-top: 20px; font-size: 0.9em; color: #2e7d32; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h2>🛡️ HUST Campus Network</h2>
            <p>Authentication Required</p>
            <input type="text" id="user" placeholder="Username (e.g., alice)">
            <input type="password" placeholder="Password">
            <button onclick="login()">Login to Network</button>
            <div id="msg" class="status">● System Status: Secure</div>
        </div>
        <script>
            function login() {
                const user = document.getElementById('user').value;
                if(user) {
                    alert('Login Successful! Welcome ' + user + '. Your device is now authorized.');
                    document.getElementById('msg').innerHTML = '● Status: Authenticated as ' + user;
                } else { alert('Please enter username'); }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"status": "success", "message": "API Login success"})

# --- LOGIC XỬ LÝ ENTROPY (ĐÃ NÂNG CẤP) ---
@app.route("/firewall/event", methods=["POST"])
def handle_event():
    data = request.json
    dest_ips = data.get("dest_ips", [])
    suspect_ip = data.get("src_ip", "Unknown")

    if not dest_ips: return jsonify({"status": "ignored"})

    # Tính toán AI
    entropy_value = calculate_entropy(dest_ips)
    print(f"\n🔍 [AI SCAN] Current Entropy: {entropy_value:.4f} | Threshold: {ENTROPY_THRESHOLD}")

    if entropy_value < ENTROPY_THRESHOLD:
        print(f"🔥 [AI ALERT] LOW ENTROPY DETECTED! (DDoS Attempt)")
        if suspect_ip not in BLOCKED_IPS and suspect_ip != "10.0.0.2":
            force_block_ip(suspect_ip)
            BLOCKED_IPS.append(suspect_ip)
            return jsonify({"status": "blocked", "entropy": entropy_value})
    else:
        print(f"✅ [AI LOG] Traffic Normal.")

    return jsonify({"status": "safe", "entropy": entropy_value})

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("\n❌ ERROR: Please run with SUDO!")
        sys.exit(1)
    print(f">>> 🚀 AI FIREWALL SERVER READY on port 5000")
    app.run(host='0.0.0.0', port=5000)
