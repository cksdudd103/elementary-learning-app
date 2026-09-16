import json
from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from ..extensions import db
from ..models import (
    Attempt,
    AttemptItem,
    Question,
    User,
    EducationOffice,
    School,
    CurriculumUnit,
    MasteryRecord,
    RecommendedCourse,
)
from .. import grade_name, subject_name

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "students": User.query.filter_by(role="student").count(),
        "questions": Question.query.filter_by(active=True).count(),
        "attempts": Attempt.query.filter(Attempt.completed_at.isnot(None)).count(),
        "average": round(
            Attempt.query.filter(Attempt.completed_at.isnot(None))
            .with_entities(func.avg(Attempt.score))
            .scalar()
            or 0
        ),
        "offices": EducationOffice.query.count(),
        "schools": School.query.count(),
        "units": CurriculumUnit.query.count(),
    }
    recent_attempts = (
        Attempt.query.filter(Attempt.completed_at.isnot(None))
        .order_by(Attempt.completed_at.desc())
        .limit(10)
        .all()
    )
    # 과목별 평균 점수
    subject_stats = (
        db.session.query(Attempt.subject, func.count(Attempt.id), func.avg(Attempt.score))
        .filter(Attempt.completed_at.isnot(None))
        .group_by(Attempt.subject)
        .all()
    )
    subject_chart = [
        {"subject": subject_name(s), "count": c, "average": round(a or 0)}
        for s, c, a in subject_stats
    ]
    # 학년별 학생 수
    grade_stats = (
        db.session.query(User.grade_level, func.count(User.id))
        .filter(User.role == "student")
        .group_by(User.grade_level)
        .order_by(User.grade_level.asc())
        .all()
    )
    grade_chart = [
        {"grade": grade_name(g), "count": c} for g, c in grade_stats
    ]
    # 취약 단원 TOP 10
    weak_units = (
        MasteryRecord.query.filter(MasteryRecord.total_questions >= 5)
        .order_by(MasteryRecord.accuracy_rate.asc())
        .limit(10)
        .all()
    )
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_attempts=recent_attempts,
        subject_chart=subject_chart,
        grade_chart=grade_chart,
        weak_units=weak_units,
    )


@admin_bp.route("/questions")
@admin_required
def questions():
    subject = request.args.get("subject")
    query = Question.query.order_by(Question.created_at.desc())
    if subject in {"math", "english", "korean", "social"}:
        query = query.filter_by(subject=subject)
    return render_template("admin/questions.html", questions=query.all(), subject=subject)


@admin_bp.route("/questions/new", methods=["GET", "POST"])
@admin_required
def question_new():
    if request.method == "POST":
        question = Question(source="admin")
        if save_question(question):
            db.session.add(question)
            db.session.commit()
            flash("문제를 등록했습니다.", "success")
            return redirect(url_for("admin.questions"))
    return render_template("admin/question_form.html", question=None)


@admin_bp.route("/questions/<int:question_id>/edit", methods=["GET", "POST"])
@admin_required
def question_edit(question_id):
    question = db.get_or_404(Question, question_id)
    if request.method == "POST" and save_question(question):
        db.session.commit()
        flash("문제를 수정했습니다.", "success")
        return redirect(url_for("admin.questions"))
    return render_template("admin/question_form.html", question=question)


@admin_bp.post("/questions/<int:question_id>/toggle")
@admin_required
def question_toggle(question_id):
    question = db.get_or_404(Question, question_id)
    question.active = not question.active
    db.session.commit()
    return redirect(url_for("admin.questions"))


def save_question(question):
    try:
        grade_level = int(request.form.get("grade_level", 1))
        difficulty = int(request.form.get("difficulty", 1))
    except ValueError:
        flash("학년과 난이도를 확인하세요.", "error")
        return False
    subject = request.form.get("subject")
    question_type = request.form.get("question_type")
    prompt = request.form.get("prompt", "").strip()
    answer = request.form.get("answer", "").strip()
    if subject not in {"math", "english", "korean", "social"} or question_type not in {"write", "choice", "listening", "speaking"}:
        flash("과목과 문제 유형을 확인하세요.", "error")
        return False
    if not 1 <= grade_level <= 9 or not prompt or not answer:
        flash("필수 항목을 모두 입력하세요.", "error")
        return False
    question.subject = subject
    question.grade_level = grade_level
    question.topic = request.form.get("topic", "").strip() or "관리자 등록"
    question.difficulty = min(max(difficulty, 1), 3)
    question.question_type = question_type
    question.prompt = prompt
    question.answer = answer
    question.explanation = request.form.get("explanation", "").strip()
    options = [value.strip() for value in request.form.get("options", "").split("|") if value.strip()]
    question.options = options if question_type == "choice" else []
    return True


@admin_bp.route("/students")
@admin_required
def students():
    student_rows = User.query.filter_by(role="student").order_by(User.created_at.desc()).all()
    return render_template("admin/students.html", students=student_rows)


def _purge_users(user_ids):
    """학생/학부모 계정과 관련 학습 데이터를 안전하게 삭제합니다."""
    if not user_ids:
        return 0
    attempt_ids = [
        row[0]
        for row in db.session.query(Attempt.id).filter(Attempt.user_id.in_(user_ids)).all()
    ]
    if attempt_ids:
        AttemptItem.query.filter(AttemptItem.attempt_id.in_(attempt_ids)).delete(
            synchronize_session=False
        )
    Attempt.query.filter(Attempt.user_id.in_(user_ids)).delete(synchronize_session=False)
    MasteryRecord.query.filter(MasteryRecord.user_id.in_(user_ids)).delete(
        synchronize_session=False
    )
    RecommendedCourse.query.filter(RecommendedCourse.user_id.in_(user_ids)).delete(
        synchronize_session=False
    )
    User.query.filter(User.parent_id.in_(user_ids)).update(
        {User.parent_id: None}, synchronize_session=False
    )
    User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
    db.session.commit()
    return len(user_ids)


@admin_bp.route("/users")
@admin_required
def users():
    role_filter = request.args.get("role", "all")
    query = User.query.order_by(User.created_at.desc())
    if role_filter in ("student", "parent"):
        query = query.filter_by(role=role_filter)
    user_rows = query.all()
    return render_template(
        "admin/users.html",
        users=user_rows,
        role_filter=role_filter,
        student_count=User.query.filter_by(role="student").count(),
        parent_count=User.query.filter_by(role="parent").count(),
    )


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def user_delete(user_id):
    user = db.get_or_404(User, user_id)
    if user.is_admin:
        flash("관리자 계정은 삭제할 수 없습니다.", "error")
        return redirect(url_for("admin.users"))
    if user.id == current_user.id:
        flash("본인 계정은 삭제할 수 없습니다.", "error")
        return redirect(url_for("admin.users"))
    display_name = user.display_name
    _purge_users([user.id])
    flash(f"{display_name} 계정과 학습 기록을 삭제했습니다.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/reset", methods=["POST"])
@admin_required
def users_reset():
    """관리자를 제외한 모든 학생/학부모 계정을 초기화합니다."""
    user_ids = [
        row[0]
        for row in db.session.query(User.id).filter(User.role != "admin").all()
    ]
    count = _purge_users(user_ids)
    flash(f"가입 계정 {count}개를 초기화했습니다. (관리자 계정은 유지)", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/students/<int:user_id>")
@admin_required
def student_detail(user_id):
    student = db.get_or_404(User, user_id)
    if student.role != "student":
        abort(404)
    attempts = (
        Attempt.query.filter_by(user_id=user_id)
        .filter(Attempt.completed_at.isnot(None))
        .order_by(Attempt.completed_at.desc())
        .all()
    )
    return render_template("admin/student_detail.html", student=student, attempts=attempts)

@admin_bp.route("/education-offices")
@admin_required
def education_offices():
    offices = EducationOffice.query.order_by(EducationOffice.region).all()
    return render_template("admin/education_offices.html", offices=offices)


@admin_bp.route("/schools")
@admin_required
def schools():
    schools = School.query.join(EducationOffice).order_by(EducationOffice.region, School.name).all()
    return render_template("admin/schools.html", schools=schools)


@admin_bp.route("/curriculum-units")
@admin_required
def curriculum_units():
    subject = request.args.get("subject")
    grade = request.args.get("grade", type=int)
    query = CurriculumUnit.query.order_by(CurriculumUnit.subject, CurriculumUnit.grade_level, CurriculumUnit.unit_order)
    if subject in {"math", "english", "korean", "social"}:
        query = query.filter_by(subject=subject)
    if grade:
        query = query.filter_by(grade_level=grade)
    return render_template("admin/curriculum_units.html", units=query.all(), subject=subject, grade=grade)


@admin_bp.route("/curriculum-units/new", methods=["GET", "POST"])
@admin_required
def curriculum_unit_new():
    if request.method == "POST":
        unit = CurriculumUnit(
            subject=request.form["subject"],
            grade_level=int(request.form["grade_level"]),
            unit_order=int(request.form["unit_order"]),
            unit_name=request.form["unit_name"].strip(),
            learning_objective=request.form.get("learning_objective", "").strip(),
            keywords=request.form.get("keywords", "").strip(),
        )
        db.session.add(unit)
        db.session.commit()
        flash("단원이 등록되었습니다.", "success")
        return redirect(url_for("admin.curriculum_units"))
    return render_template("admin/curriculum_unit_form.html", unit=None)


@admin_bp.route("/curriculum-units/<int:unit_id>/edit", methods=["GET", "POST"])
@admin_required
def curriculum_unit_edit(unit_id):
    unit = db.get_or_404(CurriculumUnit, unit_id)
    if request.method == "POST":
        unit.subject = request.form["subject"]
        unit.grade_level = int(request.form["grade_level"])
        unit.unit_order = int(request.form["unit_order"])
        unit.unit_name = request.form["unit_name"].strip()
        unit.learning_objective = request.form.get("learning_objective", "").strip()
        unit.keywords = request.form.get("keywords", "").strip()
        db.session.commit()
        flash("단원이 수정되었습니다.", "success")
        return redirect(url_for("admin.curriculum_units"))
    return render_template("admin/curriculum_unit_form.html", unit=unit)


@admin_bp.route("/curriculum-units/<int:unit_id>/delete", methods=["POST"])
@admin_required
def curriculum_unit_delete(unit_id):
    unit = db.get_or_404(CurriculumUnit, unit_id)
    db.session.delete(unit)
    db.session.commit()
    flash("단원이 삭제되었습니다.", "success")
    return redirect(url_for("admin.curriculum_units"))


@admin_bp.route("/schools/new", methods=["GET", "POST"])
@admin_required
def school_new():
    if request.method == "POST":
        school = School(
            education_office_id=int(request.form["education_office_id"]),
            name=request.form["name"].strip(),
            school_type=request.form["school_type"],
            address=request.form.get("address", "").strip(),
            phone=request.form.get("phone", "").strip(),
            homepage=request.form.get("homepage", "").strip(),
        )
        db.session.add(school)
        db.session.commit()
        flash("학교가 등록되었습니다.", "success")
        return redirect(url_for("admin.schools"))
    offices = EducationOffice.query.order_by(EducationOffice.region).all()
    return render_template("admin/school_form.html", school=None, offices=offices)


@admin_bp.route("/schools/<int:school_id>/edit", methods=["GET", "POST"])
@admin_required
def school_edit(school_id):
    school = db.get_or_404(School, school_id)
    if request.method == "POST":
        school.education_office_id = int(request.form["education_office_id"])
        school.name = request.form["name"].strip()
        school.school_type = request.form["school_type"]
        school.address = request.form.get("address", "").strip()
        school.phone = request.form.get("phone", "").strip()
        school.homepage = request.form.get("homepage", "").strip()
        db.session.commit()
        flash("학교가 수정되었습니다.", "success")
        return redirect(url_for("admin.schools"))
    offices = EducationOffice.query.order_by(EducationOffice.region).all()
    return render_template("admin/school_form.html", school=school, offices=offices)


@admin_bp.route("/schools/<int:school_id>/delete", methods=["POST"])
@admin_required
def school_delete(school_id):
    school = db.get_or_404(School, school_id)
    db.session.delete(school)
    db.session.commit()
    flash("학교가 삭제되었습니다.", "success")
    return redirect(url_for("admin.schools"))


@admin_bp.route("/education-offices/new", methods=["GET", "POST"])
@admin_required
def education_office_new():
    if request.method == "POST":
        office = EducationOffice(
            name=request.form["name"].strip(),
            region=request.form["region"].strip(),
            address=request.form.get("address", "").strip(),
            phone=request.form.get("phone", "").strip(),
            homepage=request.form.get("homepage", "").strip(),
        )
        db.session.add(office)
        db.session.commit()
        flash("교육청이 등록되었습니다.", "success")
        return redirect(url_for("admin.education_offices"))
    return render_template("admin/education_office_form.html", office=None)


@admin_bp.route("/education-offices/<int:office_id>/edit", methods=["GET", "POST"])
@admin_required
def education_office_edit(office_id):
    office = db.get_or_404(EducationOffice, office_id)
    if request.method == "POST":
        office.name = request.form["name"].strip()
        office.region = request.form["region"].strip()
        office.address = request.form.get("address", "").strip()
        office.phone = request.form.get("phone", "").strip()
        office.homepage = request.form.get("homepage", "").strip()
        db.session.commit()
        flash("교육청이 수정되었습니다.", "success")
        return redirect(url_for("admin.education_offices"))
    return render_template("admin/education_office_form.html", office=office)


@admin_bp.route("/education-offices/<int:office_id>/delete", methods=["POST"])
@admin_required
def education_office_delete(office_id):
    office = db.get_or_404(EducationOffice, office_id)
    db.session.delete(office)
    db.session.commit()
    flash("교육청이 삭제되었습니다.", "success")
    return redirect(url_for("admin.education_offices"))
