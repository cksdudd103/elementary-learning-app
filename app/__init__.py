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
            "difficulty_name": difficulty_name,
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
        _ensure_user_time_limit_column()
        _ensure_user_difficulty_column()
        _ensure_user_reset_token_column()
        _ensure_user_reset_token_expires_column()
        _ensure_user_grade_updated_at_column()
        _ensure_user_simple_pin_column()

    return app


def _ensure_user_simple_pin_column():
    """User 테이블에 simple_pin 컬럼이 없으면 추가합니다."""
    from sqlalchemy import text
    try:
        db.session.execute(text("SELECT simple_pin FROM \"user\" LIMIT 1"))
    except Exception:
        db.session.rollback()
        db.session.execute(
            text("ALTER TABLE \"user\" ADD COLUMN simple_pin VARCHAR(20)")
        )
        db.session.commit()


def _ensure_user_grade_updated_at_column():
    """User 테이블에 grade_updated_at 컬럼이 없으면 추가합니다."""
    from sqlalchemy import text
    is_postgres = db.engine.dialect.name == "postgresql"
    ts_type = "TIMESTAMP WITH TIME ZONE" if is_postgres else "TIMESTAMP"
    try:
        db.session.execute(text("SELECT grade_updated_at FROM \"user\" LIMIT 1"))
    except Exception:
        db.session.rollback()
        db.session.execute(
            text(f"ALTER TABLE \"user\" ADD COLUMN grade_updated_at {ts_type} NOT NULL DEFAULT CURRENT_TIMESTAMP")
        )
        db.session.commit()


def _ensure_user_reset_token_column():
    """User 테이블에 reset_token 컬럼이 없으면 추가합니다."""
    from sqlalchemy import text
    try:
        db.session.execute(text("SELECT reset_token FROM \"user\" LIMIT 1"))
    except Exception:
        db.session.rollback()
        db.session.execute(
            text("ALTER TABLE \"user\" ADD COLUMN reset_token VARCHAR(120) UNIQUE")
        )
        db.session.commit()


def _ensure_user_reset_token_expires_column():
    """User 테이블에 reset_token_expires_at 컬럼이 없으면 추가합니다."""
    from sqlalchemy import text
    is_postgres = db.engine.dialect.name == "postgresql"
    ts_type = "TIMESTAMP WITH TIME ZONE" if is_postgres else "TIMESTAMP"
    try:
        db.session.execute(text("SELECT reset_token_expires_at FROM \"user\" LIMIT 1"))
    except Exception:
        db.session.rollback()
        db.session.execute(
            text(f"ALTER TABLE \"user\" ADD COLUMN reset_token_expires_at {ts_type}")
        )
        db.session.commit()


def _ensure_user_time_limit_column():
    """User 테이블에 time_limit_seconds 컬럼이 없으면 추가합니다."""
    from sqlalchemy import text
    try:
        db.session.execute(text("SELECT time_limit_seconds FROM \"user\" LIMIT 1"))
    except Exception:
        db.session.rollback()
        db.session.execute(
            text("ALTER TABLE \"user\" ADD COLUMN time_limit_seconds INTEGER NOT NULL DEFAULT 3600")
        )
        db.session.commit()


def _ensure_user_difficulty_column():
    """User 테이블에 difficulty 컬럼이 없으면 추가합니다."""
    from sqlalchemy import text
    try:
        db.session.execute(text("SELECT difficulty FROM \"user\" LIMIT 1"))
    except Exception:
        db.session.rollback()
        db.session.execute(
            text("ALTER TABLE \"user\" ADD COLUMN difficulty VARCHAR(10) NOT NULL DEFAULT 'medium'")
        )
        db.session.commit()


def grade_name(grade):
    if 1 <= grade <= 6:
        return f"초{grade}"
    return f"중{grade - 6}"


def difficulty_name(difficulty):
    return {"high": "상", "medium": "중", "low": "하"}.get(difficulty, "중")


def subject_name(subject):
    return {
        "math": "수학",
        "english": "영어",
        "korean": "국어",
        "social": "사회",
        "comprehensive": "종합 평가",
    }.get(subject, subject)