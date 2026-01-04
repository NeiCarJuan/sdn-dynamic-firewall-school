from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sdn_captive_portal_secret"  # BẮT BUỘC cho session

logged_users = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        if user == "admin" and pw == "123":
            session["authenticated"] = True
            session["username"] = user

            if user not in logged_users:
                logged_users.append(user)

            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    # 🚫 Chưa login thì bị chặn
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        users=logged_users,
        current_user=session.get("username")
    )


@app.route("/logout")
def logout():
    user = session.get("username")

    session.clear()

    if user in logged_users:
        logged_users.remove(user)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
