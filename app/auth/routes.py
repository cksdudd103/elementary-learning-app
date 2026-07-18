from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_

from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        display_name = request.form.get("display_name", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")
        try:
            grade_level = int(request.form.get("grade_level", 1))
        except ValueError:
            grade_level = 1
        if not username or not email or not display_name or len(password) < 8:
            flash("모든 항목을 입력하고 비밀번호는 8자 이상으로 설정하세요.", "error")
        elif role not in {"student", "parent"}:
            flash("회원 유형을 선택하세요.", "error")
        elif role == "student" and not 1 <= grade_level <= 9:
            flash("올바른 학년을 선택하세요.", "error")
        elif User.query.filter(or_(User.username == username, User.email == email)).first():
            flash("이미 사용 중인 아이디 또는 이메일입니다.", "error")
        else:
            user = User(
                username=username,
                email=email,
                display_name=display_name,
                role=role,
                grade_level=grade_level if role == "student" else 1,
                ui_language=request.form.get("ui_language", "ko"),
            )
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            if role == "parent":
                for index in range(1, 5):
                    child_name = request.form.get(f"child_name_{index}", "").strip()
                    if not child_name:
                        continue
                    try:
                        child_grade = int(request.form.get(f"child_grade_{index}", 1))
                    except ValueError:
                        child_grade = 1
                    if not 1 <= child_grade <= 9:
                        child_grade = 1
                    child = User(
                        username=f"{user.username}_child_{index}",
                        email=f"{user.email}.child{index}@parent.local",
                        display_name=child_name,
                        role="student",
                        grade_level=child_grade,
                        ui_language=user.ui_language,
                        parent_id=user.id,
                    )
                    child.set_password(password)
                    db.session.add(child)
            db.session.commit()
            login_user(user)
            flash("회원가입이 완료되었습니다.", "success")
            return redirect(url_for("student.dashboard"))
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard"))
    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        user = User.query.filter(or_(User.username == identity, User.email == identity.lower())).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(url_for("student.dashboard"))
        flash("아이디 또는 비밀번호를 확인하세요.", "error")
    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))