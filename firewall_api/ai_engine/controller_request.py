import yaml
import subprocess
from datetime import datetime
import os

# Đường dẫn file cấu hình Faucet
FAUCET_CONFIG = "/etc/faucet/faucet.yaml"
FAUCET_SERVICE = "faucet"

def request_faucet_block(src_ip, vlan_name, confidence):
    """
    AI yêu cầu Faucet chặn IP bằng cách chèn rule vào ACL 'block_to_accounting'
    """
    print(f"[ESCALATE] Blocking {src_ip} (confidence={confidence})")

    # 1. Kiểm tra file tồn tại
    if not os.path.exists(FAUCET_CONFIG):
        print(f"[ERROR] Config file not found at {FAUCET_CONFIG}")
        return {"status": "error", "message": "Config not found"}

    # 2. Load YAML (Dùng thư viện pyyaml)
    try:
        with open(FAUCET_CONFIG, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"[ERROR] YAML Load Failed: {e}")
        return {"status": "error", "message": str(e)}

    # 3. Đảm bảo cấu trúc ACL tồn tại
    # Tên ACL phải khớp với file faucet.yaml của bạn là 'block_to_accounting'
    TARGET_ACL = "block_to_accounting" 
    
    if "acls" not in config:
        config["acls"] = {}
    
    if TARGET_ACL not in config["acls"]:
        config["acls"][TARGET_ACL] = []

    # 4. Tránh block trùng IP (Idempotency)
    current_acl = config["acls"][TARGET_ACL]
    for r in current_acl:
        # Kiểm tra xem rule đã tồn tại chưa
        if r.get("rule", {}).get("nw_dst") == "10.0.0.3" and \
           r.get("rule", {}).get("nw_src") == src_ip and \
           r.get("rule", {}).get("actions", {}).get("allow") == False:
            print(f"[INFO] IP {src_ip} already blocked.")
            return {"status": "already_blocked"}

    # 5. Tạo rule chặn mới
    # Chặn src_ip truy cập vào Server Kế toán (10.0.0.3)
    new_rule = {
        "rule": {
            "dl_type": 0x0800,      # IPv4
            "nw_src": src_ip,       # IP kẻ tấn công
            "nw_dst": "10.0.0.3",   # IP Server đích (Server Kế toán)
            "actions": {
                "allow": False
            }
        }
    }

    # 6. QUAN TRỌNG: Chèn lên đầu danh sách (Priority cao nhất)
    # Nếu dùng append(), rule này có thể nằm sau rule 'allow: true' -> Vô dụng
    config["acls"][TARGET_ACL].insert(0, new_rule)

    # 7. Ghi lại file YAML
    with open(FAUCET_CONFIG, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    # 8. Restart Faucet để áp dụng
    restart_faucet()

    return {
        "status": "blocked",
        "ip": src_ip,
        "time": datetime.now().isoformat()
    }

def restart_faucet():
    """
    Khởi động lại service Faucet
    """
    print("[FAUCET] Reloading configuration...")
    # Dùng 'reload' thay vì 'restart' để đỡ gián đoạn mạng
    cmd = ["sudo", "systemctl", "reload", FAUCET_SERVICE]
    
    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )
