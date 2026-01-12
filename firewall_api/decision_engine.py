import os
from ai_engine.controller_request import request_faucet_block
from ai_engine.ai_detector import detect_anomaly # Import module AI bạn vừa copy

USER_CONTEXT = {}
BLOCKED_IPS = set()
AI_LOG = []

# Đảm bảo đường dẫn model đúng
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def handle_user_context(data):
    """Lưu thông tin user khi login từ Portal"""
    ip = data.get("ip")
    USER_CONTEXT[ip] = {
        "username": data.get("username"),
        "role": data.get("role")
    }
    return {"status": "ok"}

def handle_attack_event(data):
    """
    Xử lý sự kiện từ IDS Watcher gửi sang
    """
    src_ip = data.get("src_ip")
    # Lấy số lượng gói tin (nếu IDS gửi sang), mặc định là 100 nếu không có
    packet_count = data.get("packet_count", 100) 
    
    # 1. Lấy ngữ cảnh người dùng
    user = USER_CONTEXT.get(src_ip, {})
    role = user.get("role", "unknown")

    print(f"[AI DECISION] Analyzing {src_ip} (Role: {role})...")

    # 2. Admin luôn được miễn tử (Whithlist)
    if role == "admin":
        print(f"[AI] {src_ip} is Admin -> ALLOW")
        return {"decision": "ALLOW", "reason": "admin_privilege"}

    # 3. Sử dụng AI Detector (Adaptive Learning)
    # Hàm này sẽ so sánh với threshold lịch sử trong model_state.json
    is_anomaly, score = detect_anomaly(packet_count)

    decision = "MONITOR"
    reason = f"score({score:.2f})"

    # Logic kết hợp: Nếu AI thấy bất thường VÀ Role là Student/Unknown -> CHẶN
    if is_anomaly:
        decision = "BLOCK"
        reason = f"Anomaly Detected (Score {score:.2f} > Threshold)"
        
        # Thực hiện chặn trên Switch Faucet
        request_faucet_block(src_ip, "accounting", score)
        BLOCKED_IPS.add(src_ip)

    # 4. Ghi log
    log_entry = {
        "ip": src_ip,
        "role": role,
        "traffic_score": score,
        "decision": decision,
        "reason": reason
    }
    AI_LOG.append(log_entry)
    
    print(f"[AI RESULT] {decision} -> {reason}")
    return {"decision": decision, "details": log_entry}

# --- Các hàm hỗ trợ Dashboard ---
def get_status(ip):
    return {
        "ip": ip,
        "role": USER_CONTEXT.get(ip, {}).get("role", "guest"),
        "blocked": ip in BLOCKED_IPS
    }

def get_blocked():
    return list(BLOCKED_IPS)

def get_logs():
    return AI_LOG
