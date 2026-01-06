from flask import Flask, request, jsonify
from decision_engine import handle_user_context, handle_attack_event

app = Flask(__name__)


@app.route("/firewall/context", methods=["POST"])
def receive_context():
    data = request.json
    result = handle_user_context(data)
    return jsonify(result)


@app.route("/firewall/event", methods=["POST"])
def receive_event():
    data = request.json
    result = handle_attack_event(data)
    return jsonify(result)


@app.route("/firewall/status", methods=["GET"])
def status():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)

