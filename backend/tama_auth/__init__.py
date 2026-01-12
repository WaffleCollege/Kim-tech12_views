from flask_login import LoginManager
from .models import User
from .routes import auth_bp

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


def init_auth(app):
    """
    親アプリ側から呼び出して:
      ・LoginManagerを紐づける
      ・Blueprintを登録する
    """
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
