from flask import Flask, request, jsonify
import decision_engine

app = Flask(__name__)

# Nhận context từ Captive Portal
@app.route("/firewall/context", methods=["POST"])
def context():
    data = request.json
    return jsonify(decision_engine.handle_user_context(data))


# Nhận sự kiện tấn công
@app.route("/firewall/event", methods=["POST"])
def event():
    data = request.json
    return jsonify(decision_engine.handle_attack_event(data))


# Trạng thái 1 IP
@app.route("/firewall/status")
def status():
    ip = request.args.get("ip")
    return jsonify(decision_engine.get_status(ip))


# Danh sách IP bị block
@app.route("/firewall/blocked")
def blocked():
    return jsonify(decision_engine.get_blocked())


# Log AI
@app.route("/firewall/logs")
def logs():
    return jsonify(decision_engine.get_logs())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

