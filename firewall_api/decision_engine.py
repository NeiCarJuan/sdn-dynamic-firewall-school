from ai_engine.decision_engine import decide
from ai_engine.local_block import local_block
from ai_engine.controller_request import request_faucet_block


def handle_user_context(data):
    """
    Nhận context người dùng từ Portal
    (vai trò, IP, phòng ban...)
    """
    print("[CONTEXT]", data)
    return {
        "status": "ok",
        "message": "User context received"
    }


def handle_attack_event(data):
    """
    Xử lý sự kiện tấn công do Portal / IDS gửi lên
    """

    attack_type = data.get("type")
    src_ip = data.get("src_ip")
    confidence = float(data.get("confidence", 0))

    print(f"[EVENT] type={attack_type}, src={src_ip}, confidence={confidence}")

    # 1. AI đưa ra quyết định
    decision = decide(attack_type, confidence)

    print(f"[AI DECISION] {decision}")

    # 2. Xử lý theo quyết định AI
    if decision == "AI_BLOCK":
        # Chặn cục bộ (demo)
        local_block(src_ip)
        return {
            "decision": "AI_BLOCK",
            "ip": src_ip
        }

    elif decision == "ESCALATE_TO_CONTROLLER":
        # Yêu cầu Faucet chặn
        result = request_faucet_block(src_ip, "accounting", confidence)
        return {
            "decision": "ESCALATED",
            "controller": "faucet",
            "result": result
        }

    # 3. Trường hợp còn lại
    return {
        "decision": "MONITOR",
        "ip": src_ip
    }

