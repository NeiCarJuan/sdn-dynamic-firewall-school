import json
import time
from ai_detector import detect_anomaly

STATE_FILE = "firewall_state.json"

def load_state():
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    print("[*] AI Defensive Firewall started")
    event_counter = 0

    while True:
        time.sleep(1)
        event_counter += 1

        anomaly, score = detect_anomaly(event_counter)
        print(f"[*] Observed behavior score = {score:.2f}")

        if anomaly:
            state = load_state()
            state["accounting_protected"] = True
            state["blocked_hosts"].append("10.0.0.100")
            save_state(state)

            print("[!] AI DETECTED ANOMALY")
            print("[!] Firewall activated adaptively")
            break

