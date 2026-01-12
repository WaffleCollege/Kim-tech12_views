from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

Base = declarative_base()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ★ ここで CORS を有効化
    CORS(
        app,
        supports_credentials=True,
        origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ]
    )

    db.init_app(app)

    from .tama_auth import init_auth
    init_auth(app)


    from . import blogs
    app.register_blueprint(blogs.blog_bp)

    with app.app_context():
        db.create_all()

    return app
