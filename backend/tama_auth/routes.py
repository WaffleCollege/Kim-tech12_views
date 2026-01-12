from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from .models import User
from .. import db


auth_bp = Blueprint(
    "auth", 
    __name__, 
    url_prefix="/auth",
    template_folder="templates"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        pw = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(pw):
            flash("メールまたはパスワードが違います", "error")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("auth.dashboard"))

    return render_template("tama_login.html")

from flask import jsonify

@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    pw = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(pw):
        return jsonify({"ok": False, "message": "認証失敗"}), 401

    login_user(user)
    return jsonify({
        "ok": True,
        "user": {"id": user.id, "email": user.email}
    })


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return "ログイン成功 🎉"

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # 入力チェック
    if not name or not email or not password:
        return jsonify({"error": "missing fields"}), 400

    # 既存メール確認
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    # ユーザー作成
    user = User(name=name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created"}), 201

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.dashboard"))
