from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from flaskr import db
from flaskr.tama_models import User

tama_auth_bp = Blueprint("tama_auth", __name__, url_prefix="/auth")


@tama_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # 認証失敗
        if not user or not user.check_password(password):
            flash("メールアドレスまたはパスワードが違います", "error")
            return redirect(url_for("tama_auth.login"))

        # 認証成功 → セッションへ
        login_user(user)
        return redirect(url_for("tama_auth.dashboard"))

    return render_template("tama_login.html")


@tama_auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました", "success")
    return redirect(url_for("tama_auth.login"))


@tama_auth_bp.route("/dashboard")
@login_required
def dashboard():
    return f"ようこそ {current_user.email} さん 🎉"
