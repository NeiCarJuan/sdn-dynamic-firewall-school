from ai_engine.controller_request import request_faucet_block

USER_CONTEXT = {}
BLOCKED_IPS = set()
AI_LOG = []

def handle_user_context(data):
    ip = data.get("ip")
    USER_CONTEXT[ip] = {
        "username": data.get("username"),
        "role": data.get("role")
    }
    return {"status": "ok"}

def handle_attack_event(data):
    src_ip = data.get("src_ip")
    confidence = float(data.get("confidence", 0))

    user = USER_CONTEXT.get(src_ip, {})
    role = user.get("role", "unknown")

    decision = "MONITOR"

    if role == "student" and confidence >= 0.7:
        decision = "BLOCK"
    if role == "staff" and confidence >= 0.9:
        decision = "BLOCK"
    if role == "admin":
        decision = "ALLOW"

    if decision == "BLOCK":
        request_faucet_block(src_ip, "accounting", confidence)
        BLOCKED_IPS.add(src_ip)

    AI_LOG.append({
        "ip": src_ip,
        "role": role,
        "confidence": confidence,
        "decision": decision
    })

    return {"decision": decision}

# 🔥 API cho Dashboard
def get_status(ip):
    return {
        "ip": ip,
        "role": USER_CONTEXT.get(ip, {}).get("role"),
        "blocked": ip in BLOCKED_IPS
    }

def get_blocked():
    return list(BLOCKED_IPS)

def get_logs():
    return AI_LOG

