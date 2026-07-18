import os

from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import current_user

from .config import Config
from .extensions import csrf, db, login_manager
from .i18n import get_locale, translate
from .models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if not app.config["TESTING"] and os.environ.get("FLASK_ENV") == "production":
        if app.config["SECRET_KEY"] == "local-development-secret-change-me":
            raise RuntimeError("운영 환경에서는 SECRET_KEY를 설정해야 합니다.")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "로그인이 필요합니다."

    from .auth.routes import auth_bp
    from .parent.routes import parent_bp
    from .student.routes import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(parent_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.context_processor
    def inject_helpers():
        import random
        return {
            "t": translate,
            "current_language": get_locale(),
            "grade_name": grade_name,
            "subject_name": subject_name,
            "random_count": lambda: random.choice([10, 20, 30]),
        }

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("student.dashboard"))
        return render_template("index.html")

    @app.route("/language/<language>")
    def language(language):
        if language in {"ko", "en"}:
            session["language"] = language
            if current_user.is_authenticated:
                current_user.ui_language = language
                db.session.commit()
        return redirect(request.referrer or url_for("index"))

    with app.app_context():
        db.create_all()

    return app


def grade_name(grade):
    return f"초등 {grade}학년" if grade <= 6 else f"중등 {grade - 6}학년"


def subject_name(subject):
    return {
        "math": "수학",
        "english": "영어",
        "korean": "국어",
        "social": "사회",
        "comprehensive": "종합 평가",
    }.get(subject, subject)