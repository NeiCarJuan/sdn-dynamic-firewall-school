from flask import Flask, render_template, request, redirect, session
from controller_api import send_user_context

app = Flask(__name__)
app.secret_key = "secret_key_for_demo"


# =========================
# ROUTE: LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ===== DEMO AUTHENTICATION =====
        if username == "admin" and password == "123":
            session["authenticated"] = True
            session["username"] = username

            # ===== GÁN NGỮ CẢNH NGƯỜI DÙNG =====
            role = "staff"                     # mock role
            ip = request.remote_addr           # IP client

            session["role"] = role
            session["ip"] = ip

            # ===== GỬI THÔNG TIN SANG FIREWALL MODULE =====
            send_user_context(username, role, ip)

            return redirect("/dashboard")

        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# =========================
# ROUTE: DASHBOARD
# =========================
@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect("/")

    return render_template(
        "dashboard.html",
        user=session.get("username"),
        role=session.get("role"),
        ip=session.get("ip")
    )


# =========================
# ROUTE: LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

