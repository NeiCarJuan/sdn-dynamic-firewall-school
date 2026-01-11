from flask import Flask, request, render_template, redirect, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

FW = "http://127.0.0.1:9000"

# -----------------------------
# LOGIN
# -----------------------------

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    role = request.form["role"]
    ip = request.form["ip"]

    # Gửi context sang Firewall AI
    try:
        requests.post(FW + "/firewall/context", json={
            "username": username,
            "role": role,
            "ip": ip
        })
    except:
        pass

    # Chỉ admin mới được vào dashboard
    if role == "admin":
        return redirect(f"/dashboard?ip={ip}&u={username}&r={role}")

    return f"Login OK. Role={role}"


# -----------------------------
# DASHBOARD
# -----------------------------

@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        ip=request.args.get("ip"),
        username=request.args.get("u"),
        role=request.args.get("r")
    )


# -----------------------------
# PROXY API (Browser → Portal → Firewall)
# -----------------------------

@app.route("/status", methods=["GET","POST","OPTIONS"])
def status():
    try:
        r = requests.get(FW + "/firewall/status", params=request.args)
        return Response(r.content, status=r.status_code, content_type="application/json")
    except:
        return Response('{"error":"firewall not reachable"}', status=500, content_type="application/json")


@app.route("/blocked", methods=["GET","POST","OPTIONS"])
def blocked():
    try:
        r = requests.get(FW + "/firewall/blocked")
        return Response(r.content, status=r.status_code, content_type="application/json")
    except:
        return Response('{"error":"firewall not reachable"}', status=500, content_type="application/json")


@app.route("/logs", methods=["GET","POST","OPTIONS"])
def logs():
    try:
        r = requests.get(FW + "/firewall/logs")
        return Response(r.content, status=r.status_code, content_type="application/json")
    except:
        return Response('{"error":"firewall not reachable"}', status=500, content_type="application/json")


# -----------------------------
# START
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

