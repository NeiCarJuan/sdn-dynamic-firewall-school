import json
from datetime import datetime

def request_faucet_block(src_ip, target, confidence):
    event = {
        "time": datetime.now().isoformat(),
        "event": "unknown_attack",
        "source_ip": src_ip,
        "target": target,
        "confidence": confidence
    }

    print("[AI → FAUCET] Escalation request:")
    print(json.dumps(event, indent=2))

