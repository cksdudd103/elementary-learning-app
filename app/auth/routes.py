from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from secrets import token_urlsafe
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy import or_

from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return redirect(url_for("auth.register_choice"))


@auth_bp.route("/register/student", methods=["GET", "POST"])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        password = request.form.get("password", "")
        try:
            grade_level = int(request.form.get("grade_level", 1))
        except ValueError:
            grade_level = 1
        pin = _normalize_pin(request.form.get("simple_pin", ""))
        if not display_name or len(password) < 8:
            flash("이름과 비밀번호(8자 이상)를 입력하세요.", "error")
        elif not 1 <= grade_level <= 9:
            flash("올바른 학년을 선택하세요.", "error")
        elif not pin or len(pin) != 4 or not pin.isdigit():
            flash("4자리 PIN을 입력하세요.", "error")
        else:
            username, email = _generate_unique_student_credentials()
            user = User(
                username=username,
                email=email,
                display_name=display_name,
                role="student",
                grade_level=grade_level,
                ui_language=request.form.get("ui_language", "ko"),
                simple_pin=pin,
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("회원가입이 완료되었습니다.", "success")
            return redirect(url_for("student.dashboard"))
    return render_template("auth/register_student.html")


@auth_bp.route("/register/parent", methods=["GET", "POST"])
def register_parent():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        display_name = request.form.get("display_name", "").strip()
        password = request.form.get("password", "")
        if not username or not email or not display_name or len(password) < 8:
            flash("모든 항목을 입력하고 비밀번호는 8자 이상으로 설정하세요.", "error")
        elif User.query.filter(or_(User.username == username, User.email == email)).first():
            flash("이미 사용 중인 아이디 또는 이메일입니다.", "error")
        else:
            user = User(
                username=username,
                email=email,
                display_name=display_name,
                role="parent",
                grade_level=1,
                ui_language=request.form.get("ui_language", "ko"),
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            linked = 0
            skipped = 0
            for index in range(1, 5):
                child_name = request.form.get(f"child_name_{index}", "").strip()
                if not child_name:
                    continue
                try:
                    child_grade = int(request.form.get(f"child_grade_{index}", 1))
                except ValueError:
                    child_grade = 1
                child_pin = _normalize_pin(request.form.get(f"child_pin_{index}", ""))
                if not 1 <= child_grade <= 9:
                    child_grade = 1
                child = User.query.filter(
                    User.role == "student",
                    User.display_name == child_name,
                    User.grade_level == child_grade,
                    User.simple_pin == child_pin,
                    User.parent_id.is_(None),
                ).first()
                if child:
                    child.parent_id = user.id
                    linked += 1
                else:
                    skipped += 1
            if skipped:
                flash(f"{linked}명의 자녀와 연동되었습니다. 일치하는 학생 계정이 없거나 이미 연동된 항목은 제외되었습니다.", "info")
            elif linked:
                flash(f"{linked}명의 자녀와 연동되었습니다.", "success")
            db.session.commit()
            login_user(user)
            flash("회원가입이 완료되었습니다.", "success")
            if linked:
                return redirect(url_for("parent.dashboard"))
            return redirect(url_for("student.dashboard"))
    return render_template("auth/register_parent.html")


@auth_bp.route("/register/choice")
def register_choice():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        # 학생 간편 로그인 (이름 + 학년 + PIN)
        display_name = request.form.get("display_name", "").strip()
        if display_name:
            try:
                grade_level = int(request.form.get("grade_level", 1))
            except ValueError:
                grade_level = 1
            pin = _normalize_pin(request.form.get("simple_pin", ""))
            if not pin or len(pin) != 4 or not pin.isdigit():
                flash("4자리 PIN을 입력하세요.", "error")
                return render_template("auth/login.html", tab="student")
            user = User.query.filter_by(
                role="student", display_name=display_name, grade_level=grade_level, simple_pin=pin
            ).first()
            if user:
                if user.update_grade_annually():
                    db.session.commit()
                login_user(user, remember=False)
                return redirect(url_for("student.dashboard"))
            flash("이름, 학년, PIN을 확인하세요.", "error")
            return render_template("auth/login.html", tab="student")

        # 일반 로그인 (아이디/이메일 + 비밀번호)
        identity = request.form.get("identity", "").strip()
        user = User.query.filter(or_(User.username == identity, User.email == identity.lower())).first()
        if user and user.check_password(request.form.get("password", "")):
            if user.update_grade_annually():
                db.session.commit()
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(url_for("student.dashboard"))
        flash("아이디 또는 비밀번호를 확인하세요.", "error")
    return render_template("auth/login.html", tab="general")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            user.reset_token = token_urlsafe(32)
            user.reset_token_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
            db.session.commit()
            # TODO: 실제 이메일 서비스 연동 시 아래 print 제거
            reset_url = url_for("auth.reset_password", token=user.reset_token, _external=True)
            print(f"[PASSWORD RESET] {reset_url}")
            flash("입력하신 이메일로 재설정 안내를 별냈습니다.", "success")
        else:
            # 동일한 메시지로 이메일 존재 여부 노출 방지
            flash("입력하신 이메일로 재설정 안내를 별냈습니다.", "success")
    return render_template("auth/forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expires_at or user.reset_token_expires_at < datetime.now(timezone.utc):
        flash("유효하지 않거나 만료된 링크입니다.", "error")
        return redirect(url_for("auth.forgot_password"))
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if len(password) < 8:
            flash("비밀번호는 8자 이상이어야 합니다.", "error")
        elif password != confirm:
            flash("비밀번호가 일치하지 않습니다.", "error")
        else:
            user.set_password(password)
            user.reset_token = None
            user.reset_token_expires_at = None
            db.session.commit()
            flash("비밀번호가 변경되었습니다. 다시 로그인하세요.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", token=token)


@auth_bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


def _normalize_pin(pin):
    """PIN에서 공백을 제거하고 숫자 4자리만 남깁니다."""
    return "".join(ch for ch in (pin or "") if ch.isdigit())[:4]


def _generate_unique_student_credentials():
    """학생 가입 시 자동으로 고유한 아이디와 이메일을 생성합니다."""
    while True:
        suffix = uuid4().hex[:12]
        username = f"stu_{suffix}"
        email = f"{suffix}@student.harusso.kr"
        if not User.query.filter(or_(User.username == username, User.email == email)).first():
            return username, email


@auth_bp.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username != current_user.username:
            flash("아이디가 일치하지 않습니다.", "error")
        elif not current_user.check_password(password):
            flash("비밀번호를 확인하세요.", "error")
        else:
            user = User.query.get(current_user.id)
            logout_user()
            db.session.delete(user)
            db.session.commit()
            flash("회원 탈퇴가 완료되었습니다.", "success")
            return redirect(url_for("index"))
    return render_template("auth/delete_account.html")