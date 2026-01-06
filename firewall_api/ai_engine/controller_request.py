import yaml
import subprocess
from datetime import datetime

FAUCET_CONFIG = "/etc/faucet/faucet.yaml"
FAUCET_SERVICE = "faucet"


def request_faucet_block(src_ip, vlan_name, confidence):
    """
    AI yêu cầu Faucet chặn một IP cụ thể
    """

    print(f"[ESCALATE] Blocking {src_ip} (confidence={confidence})")

    # 1. Load faucet.yaml
    with open(FAUCET_CONFIG, "r") as f:
        config = yaml.safe_load(f)

    if config is None:
        raise RuntimeError("Faucet config is empty or invalid")

    # 2. Đảm bảo ACL tồn tại
    if "acls" not in config:
        config["acls"] = {}

    if "dynamic_block" not in config["acls"]:
        config["acls"]["dynamic_block"] = []

    # 3. Tạo rule chặn
    rule = {
        "rule": {
            "nw_src": src_ip,
            "actions": {
                "allow": False
            }
        }
    }

    # 4. Tránh block trùng IP
    for r in config["acls"]["dynamic_block"]:
        if r.get("rule", {}).get("nw_src") == src_ip:
            print("[INFO] IP already blocked")
            return {"status": "already_blocked"}

    # 5. Ghi rule mới
    config["acls"]["dynamic_block"].append(rule)

    with open(FAUCET_CONFIG, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    # 6. Restart Faucet
    restart_faucet()

    return {
        "status": "blocked",
        "ip": src_ip,
        "time": datetime.now().isoformat()
    }


def restart_faucet():
    """
    Restart Faucet service (demo-safe)
    """
    print("[FAUCET] Restarting controller...")

    subprocess.run(
        ["sudo", "systemctl", "restart", FAUCET_SERVICE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

