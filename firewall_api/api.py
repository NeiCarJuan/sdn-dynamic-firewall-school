from flask import Flask, request, jsonify
import time

app = Flask(__name__)

blocked_ips = []
event_logs = []

@app.route("/firewall/event", methods=["POST"])
def handle_ids_alert():
    data = request.json
    attacker_ip = data.get("src_ip")
    reason = data.get("reason", "Unknown")
    confidence = data.get("confidence", 0)

    print(f"⚠️ IDS ALERT → {attacker_ip} | {reason} | confidence={confidence}")

    # Ghi log
    event_logs.append({
        "ip": attacker_ip,
        "reason": reason,
        "confidence": confidence,
        "time": time.strftime("%H:%M:%S")
    })

    # Nếu chưa bị block thì thêm vào blacklist
    if attacker_ip not in blocked_ips:
        blocked_ips.append(attacker_ip)
        print(f"🔥 AI FIREWALL: Blocking {attacker_ip}")

    return jsonify({
        "status": "received",
        "action": "blocked",
        "ip": attacker_ip
    }), 200


@app.route("/firewall/blocked")
def get_blocked():
    return jsonify(blocked_ips)


@app.route("/firewall/logs")
def get_logs():
    return jsonify(event_logs)


if __name__ == "__main__":
    app.run(port=9000)

