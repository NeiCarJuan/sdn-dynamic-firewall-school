from ai_engine.decision_engine import decide
from ai_engine.local_block import local_block
from ai_engine.controller_request import request_faucet_block

def simulate_attack(attack_type, src_ip, target, confidence):
    print(f"\n[SIMULATION] Attack detected: {attack_type}")

    decision = decide(attack_type, confidence)
    print(f"[DECISION] {decision}")

    if decision == "AI_BLOCK":
        local_block(src_ip)

    elif decision == "ESCALATE_TO_CONTROLLER":
        request_faucet_block(src_ip, target, confidence)

    else:
        print("[AI] Monitoring traffic...")

# ===== TEST CASES =====

simulate_attack(
    attack_type="icmp_flood",
    src_ip="10.0.0.5",
    target="accounting",
    confidence=0.9
)

simulate_attack(
    attack_type="unknown_behavior",
    src_ip="10.0.0.6",
    target="accounting",
    confidence=0.8
)

