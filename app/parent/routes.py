from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from ..extensions import db
from ..models import Attempt, User

parent_bp = Blueprint("parent", __name__, url_prefix="/parent")


def parent_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_parent:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


@parent_bp.route("/")
@parent_required
def dashboard():
    children = User.query.filter_by(parent_id=current_user.id).order_by(User.grade_level, User.display_name).all()
    child_ids = [child.id for child in children]
    completed_counts = {}
    if child_ids:
        rows = (
            db.session.query(Attempt.user_id, func.count(Attempt.id))
            .filter(Attempt.user_id.in_(child_ids))
            .filter(Attempt.completed_at.isnot(None))
            .group_by(Attempt.user_id)
            .all()
        )
        completed_counts = {user_id: count for user_id, count in rows}
    attempts = (
        Attempt.query.filter(Attempt.user_id.in_(child_ids))
        .filter(Attempt.completed_at.isnot(None))
        .order_by(Attempt.completed_at.desc())
        .limit(20)
        .all()
    )
    stats = {
        "count": sum(completed_counts.values()),
        "average": round(
            Attempt.query.filter(Attempt.user_id.in_(child_ids))
            .filter(Attempt.completed_at.isnot(None))
            .with_entities(func.avg(Attempt.score))
            .scalar()
            or 0
        ),
        "best": Attempt.query.filter(Attempt.user_id.in_(child_ids))
        .filter(Attempt.completed_at.isnot(None))
        .with_entities(func.max(Attempt.score))
        .scalar()
        or 0,
    }
    return render_template(
        "parent/dashboard.html",
        children=children,
        attempts=attempts,
        stats=stats,
        completed_counts=completed_counts,
    )


def _normalize_pin(pin):
    """PIN에서 공백을 제거하고 숫자 4자리만 남깁니다."""
    return "".join(ch for ch in (pin or "") if ch.isdigit())[:4]


@parent_bp.route("/children/new", methods=["GET", "POST"])
@parent_required
def child_new():
    if len(current_user.children) >= 4:
        flash("학생은 최대 4명까지 연동할 수 있습니다.", "error")
        return redirect(url_for("parent.dashboard"))
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        child_pin = _normalize_pin(request.form.get("child_pin", ""))
        try:
            grade_level = int(request.form.get("grade_level", 1))
        except ValueError:
            grade_level = 1
        if not display_name:
            flash("학생 이름을 입력하세요.", "error")
        elif not 1 <= grade_level <= 9:
            flash("올바른 학년을 선택하세요.", "error")
        elif not child_pin or len(child_pin) != 4:
            flash("학생의 4자리 PIN을 입력하세요.", "error")
        else:
            child = User.query.filter(
                User.role == "student",
                User.display_name == display_name,
                User.grade_level == grade_level,
                User.simple_pin == child_pin,
                User.parent_id.is_(None),
            ).first()
            if child:
                child.parent_id = current_user.id
                db.session.commit()
                flash("자녀와 연동되었습니다.", "success")
                return redirect(url_for("parent.dashboard"))
            flash("일치하는 학생 계정을 찾을 수 없거나 이미 다른 학부모와 연동되어 있습니다. 이름, 학년, PIN을 다시 확인하세요.", "error")
    return render_template("parent/child_form.html", child=None)


@parent_bp.post("/children/<int:child_id>/unlink")
@parent_required
def child_unlink(child_id):
    child = db.get_or_404(User, child_id)
    if child.parent_id != current_user.id:
        abort(403)
    child.parent_id = None
    db.session.commit()
    flash("자녀 연동을 해제했습니다.", "success")
    return redirect(url_for("parent.dashboard"))


@parent_bp.route("/children/<int:child_id>/edit", methods=["GET", "POST"])
@parent_required
def child_edit(child_id):
    flash("학년은 학생 계정의 가입 정보에 따라 자동으로 관리됩니다.", "info")
    return redirect(url_for("parent.dashboard"))


@parent_bp.post("/children/<int:child_id>/delete")
@parent_required
def child_delete(child_id):
    flash("학생 계정 삭제는 학생 본인이 회원 탈퇴 메뉴에서 진행할 수 있습니다.", "info")
    return redirect(url_for("parent.dashboard"))


@parent_bp.route("/children/<int:child_id>")
@parent_required
def child_detail(child_id):
    child = db.get_or_404(User, child_id)
    if child.parent_id != current_user.id:
        abort(403)
    attempts = (
        Attempt.query.filter_by(user_id=child.id)
        .filter(Attempt.completed_at.isnot(None))
        .order_by(Attempt.completed_at.desc())
        .all()
    )
    return render_template("parent/child_detail.html", child=child, attempts=attempts)


@parent_bp.route("/children/<int:child_id>/reset-password", methods=["GET", "POST"])
@parent_required
def child_reset_password(child_id):
    child = db.get_or_404(User, child_id)
    if child.parent_id != current_user.id:
        abort(403)
    if request.method == "POST":
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        if not new_password:
            flash("새 비밀번호를 입력하세요.", "error")
        elif len(new_password) < 6:
            flash("비밀번호는 6자 이상이어야 합니다.", "error")
        elif new_password != confirm_password:
            flash("비밀번호가 서로 일치하지 않습니다.", "error")
        else:
            child.set_password(new_password)
            db.session.commit()
            flash(f"{child.display_name} 학생의 비밀번호가 변경되었습니다.", "success")
            return redirect(url_for("parent.dashboard"))
    return render_template("parent/child_reset_password.html", child=child)
