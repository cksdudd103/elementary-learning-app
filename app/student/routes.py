import json
import random
from functools import wraps
from datetime import datetime, timezone

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from ..extensions import db
from ..models import Attempt, AttemptItem, Question, CurriculumUnit, MasteryRecord, RecommendedCourse, ensure_aware
from ..services.english_listen_write import CATEGORIES, LEVELS, get_lessons, is_correct
from ..services.english_generator import SENTENCES, VOCABULARY, generate_english_set
from ..services.english_review import generate_conversation_review, generate_word_set
from ..services.grading import grade_answer
from ..services.image_helper import placeholder_image, topic_image
from ..services.korean_generator import generate_korean_set
from ..services.korean_review import generate_korean_review
from ..services.math_generator import generate_math_set
from ..services.math_review import generate_math_review
from ..services.social_generator import generate_social_set
from ..services.social_review import generate_social_review
from .. import grade_name, subject_name

student_bp = Blueprint("student", __name__, url_prefix="/learn")


def _grade_1_2_required(view):
    @wraps(view)
    @login_required
    def decorated_view(*args, **kwargs):
        if current_user.grade_level not in (1, 2):
            flash("이 연습은 1~2학년용입니다.", "info")
            return redirect(url_for("student.dashboard"))
        return view(*args, **kwargs)

    return decorated_view


@student_bp.route("/practice/multiplication")
@login_required
@_grade_1_2_required
def practice_multiplication():
    return render_template("student/practice_multiplication.html")


@student_bp.route("/practice/numbers")
@login_required
@_grade_1_2_required
def practice_numbers():
    return render_template("student/practice_numbers.html")


@student_bp.route("/practice/korean")
@login_required
@_grade_1_2_required
def practice_korean():
    return render_template("student/practice_korean.html")


@student_bp.before_request
def require_student_role():
    if current_user.is_authenticated and current_user.role != "student":
        flash("학생 메뉴는 학생 계정으로 로그인 후 이용할 수 있습니다.", "info")
        return redirect(url_for("parent.dashboard"))


@student_bp.route("/")
@login_required
def dashboard():
    if current_user.update_grade_annually():
        db.session.commit()
        flash(f"학년이 {grade_name(current_user.grade_level)}(으)로 자동 업데이트되었습니다.", "success")
    semester = _valid_semester(request.args.get("semester"))
    completed = Attempt.query.filter_by(user_id=current_user.id).filter(Attempt.completed_at.isnot(None))
    if semester in (1, 2):
        completed = completed.filter_by(semester=semester)
    recent_attempts = completed.order_by(Attempt.completed_at.desc()).limit(6).all()
    stats = {
        "count": completed.count(),
        "average": round(completed.with_entities(func.avg(Attempt.score)).scalar() or 0),
        "best": completed.with_entities(func.max(Attempt.score)).scalar() or 0,
    }
    mastery = (
        MasteryRecord.query.filter_by(user_id=current_user.id)
        .filter(MasteryRecord.accuracy_rate < 70)
        .order_by(MasteryRecord.accuracy_rate.asc())
        .limit(5)
        .all()
    )
    recommended = (
        RecommendedCourse.query.filter_by(user_id=current_user.id, is_completed=False)
        .order_by(RecommendedCourse.priority.asc())
        .limit(3)
        .all()
    )
    return render_template(
        "student/dashboard.html",
        recent_attempts=recent_attempts,
        stats=stats,
        semester=semester,
        mastery=mastery,
        recommended=recommended,
    )


@student_bp.post("/settings")
@login_required
def settings():
    flash("학년은 가입 시 선택한 값에 따라 자동으로 관리됩니다.", "info")
    return redirect(url_for("student.dashboard"))


def select_questions(subject, grade, count=10, difficulty="medium", semester=None, focus_wrong=False):
    generators = {
        "math": generate_math_set,
        "english": generate_english_set,
        "korean": generate_korean_set,
        "social": generate_social_set,
    }
    if subject not in generators:
        abort(404)
    # 난이도에 따라 인접 학년 콘텐츠 사용
    if difficulty == "low":
        effective_grade = max(1, grade - 1)
    elif difficulty == "high":
        effective_grade = min(9, grade + 1)
    else:
        effective_grade = grade

    # 취약 단원 우선 출제 모드
    weak_units = []
    if focus_wrong:
        weak_units = [
            r.unit_name for r in MasteryRecord.query.filter_by(
                user_id=current_user.id, subject=subject, grade_level=grade
            ).filter(MasteryRecord.accuracy_rate < 70).order_by(MasteryRecord.accuracy_rate.asc()).limit(3).all()
        ]

    generated = generators[subject](effective_grade, count, semester=semester, preferred_topics=weak_units)
    custom = Question.query.filter_by(subject=subject, grade_level=grade, active=True)
    if semester in (1, 2):
        custom = custom.filter_by(semester=semester)
    custom = custom.all()
    if custom:
        custom_count = min(len(custom), random.randint(1, max(1, count // 4)))
        for question, position in zip(random.sample(custom, custom_count), random.sample(range(count), custom_count)):
            generated[position] = {
                "prompt": question.prompt,
                "answer": question.answer,
                "topic": question.topic,
                "explanation": question.explanation,
                "question_type": question.question_type,
                "options": question.options,
                "image_url": question.image_url,
                "max_points": getattr(question, "max_points", None) or 10,
                "semester": question.semester,
            }
    return generated


def build_attempt(subject, count=None, time_limit=None, is_comprehensive=False, semester=None, focus_wrong=False):
    grade = current_user.grade_level
    difficulty = current_user.difficulty or "medium"
    count = count or 10
    time_limit = time_limit or current_user.time_limit_seconds or 3600
    attempt = Attempt(
        user_id=current_user.id,
        subject=subject,
        grade_level=grade,
        semester=semester if semester in (1, 2) else 1,
        question_count=count,
        time_limit_seconds=time_limit,
        is_comprehensive=is_comprehensive,
    )
    db.session.add(attempt)
    db.session.commit()
    if not is_comprehensive:
        questions = select_questions(subject, grade, count, difficulty=difficulty, semester=semester, focus_wrong=focus_wrong)
        for position, question in enumerate(questions, start=1):
            raw_image_url = question.get("image_url")
            # data:image/svg+xml;base64 URI는 길어질 수 있어 String(255) 컬럼에 저장하면
            # 데이터베이스 오류가 발생합니다. 255자를 초과하면 저장하지 않습니다.
            image_url = raw_image_url if raw_image_url and len(raw_image_url) <= 255 else None
            item = AttemptItem(
                position=position,
                question_type=question["question_type"],
                topic=question["topic"],
                prompt=question["prompt"],
                correct_answer=question["answer"],
                explanation=question["explanation"],
                max_points=question.get("max_points", 10),
                image_url=image_url,
            )
            item.options = question["options"]
            attempt.items.append(item)
        db.session.commit()
    return attempt


@student_bp.route("/math/review")
@login_required
def math_review():
    grade = current_user.grade_level
    semester = _valid_semester(request.args.get("semester"))
    units = CurriculumUnit.query.filter_by(subject="math", grade_level=grade)
    if semester in (1, 2):
        units = units.filter_by(semester=semester)
    units = units.order_by(CurriculumUnit.unit_order).all()
    return render_template(
        "student/math_review.html",
        concepts=generate_math_review(grade, 5),
        units=units,
        semester=semester,
    )


@student_bp.route("/math/start")
@login_required
def start_math():
    count = _valid_count(request.args.get("count", "10"))
    semester = _valid_semester(request.args.get("semester"))
    return redirect(url_for("student.attempt", attempt_id=build_attempt("math", count=count, semester=semester).id))


@student_bp.route("/korean/review")
@login_required
def korean_review():
    grade = current_user.grade_level
    semester = _valid_semester(request.args.get("semester"))
    units = CurriculumUnit.query.filter_by(subject="korean", grade_level=grade)
    if semester in (1, 2):
        units = units.filter_by(semester=semester)
    units = units.order_by(CurriculumUnit.unit_order).all()
    return render_template(
        "student/korean_review.html",
        concepts=generate_korean_review(grade, 5),
        units=units,
        semester=semester,
    )


@student_bp.route("/korean/start")
@login_required
def start_korean():
    count = _valid_count(request.args.get("count", "10"))
    semester = _valid_semester(request.args.get("semester"))
    return redirect(url_for("student.attempt", attempt_id=build_attempt("korean", count=count, semester=semester).id))


@student_bp.route("/social/review")
@login_required
def social_review():
    grade = current_user.grade_level
    semester = _valid_semester(request.args.get("semester"))
    units = CurriculumUnit.query.filter_by(subject="social", grade_level=grade)
    if semester in (1, 2):
        units = units.filter_by(semester=semester)
    units = units.order_by(CurriculumUnit.unit_order).all()
    return render_template(
        "student/social_review.html",
        concepts=generate_social_review(grade, 5),
        units=units,
        semester=semester,
    )


@student_bp.route("/social/start")
@login_required
def start_social():
    count = _valid_count(request.args.get("count", "10"))
    semester = _valid_semester(request.args.get("semester"))
    return redirect(url_for("student.attempt", attempt_id=build_attempt("social", count=count, semester=semester).id))


@student_bp.route("/english/review")
@login_required
def english_review():
    grade = current_user.grade_level
    semester = _valid_semester(request.args.get("semester"))
    units = CurriculumUnit.query.filter_by(subject="english", grade_level=grade)
    if semester in (1, 2):
        units = units.filter_by(semester=semester)
    units = units.order_by(CurriculumUnit.unit_order).all()
    return render_template(
        "student/english_review.html",
        words=generate_word_set(grade),
        conversations=generate_conversation_review(grade),
        sentences=[s for s, _ in random.sample(SENTENCES[grade], min(10, len(SENTENCES[grade])))],
        units=units,
        semester=semester,
    )


@student_bp.route("/english/word-check", methods=["POST"])
@login_required
def english_word_check():
    learned = request.form.getlist("learned")
    count = len(learned)
    flash(f"{count}개의 단어를 외웠어요! 훌륭해요.", "success")
    return redirect(url_for("student.english_review"))


@student_bp.route("/english/start")
@login_required
def start_english():
    count = _valid_count(request.args.get("count", "10"))
    semester = _valid_semester(request.args.get("semester"))
    return redirect(url_for("student.attempt", attempt_id=build_attempt("english", count=count, semester=semester).id))


@student_bp.route("/comprehensive/start")
@login_required
def start_comprehensive():
    subjects = ["korean", "english", "math", "social"]
    per_subject = 7
    total = per_subject * len(subjects)  # 28
    extra = 30 - total  # 2
    attempt = build_attempt("comprehensive", count=30, time_limit=5400, is_comprehensive=True)
    # 기존 더미 items를 비우고 4과목 무작위 문제 30개로 재구성
    attempt.items = []
    items = []
    for i, subject in enumerate(subjects):
        n = per_subject + (1 if i < extra else 0)
        items.extend(select_questions(subject, current_user.grade_level, n, difficulty=current_user.difficulty or "medium"))
    random.shuffle(items)
    for position, question in enumerate(items[:30], start=1):
        raw_image_url = question.get("image_url")
        image_url = raw_image_url if raw_image_url and len(raw_image_url) <= 255 else None
        item = AttemptItem(
            position=position,
            question_type=question["question_type"],
            topic=question["topic"],
            prompt=question["prompt"],
            correct_answer=question["answer"],
            explanation=question["explanation"],
            max_points=question.get("max_points", 10),
            image_url=image_url,
        )
        item.options = question["options"]
        attempt.items.append(item)
    db.session.commit()
    return redirect(url_for("student.attempt", attempt_id=attempt.id))


def _valid_count(value):
    try:
        count = int(value)
    except ValueError:
        return 10
    return count if count in (10, 20, 30) else 10


def _valid_semester(value):
    try:
        semester = int(value)
    except (ValueError, TypeError):
        return None
    return semester if semester in (1, 2) else None


def _check_time_limit(attempt):
    if attempt.completed_at:
        return True
    elapsed = (datetime.now(timezone.utc) - ensure_aware(attempt.started_at)).total_seconds()
    return elapsed >= attempt.time_limit_seconds


@student_bp.route("/attempt/<int:attempt_id>", methods=["GET", "POST"])
@login_required
def attempt(attempt_id):
    current_attempt = db.get_or_404(Attempt, attempt_id)
    if current_attempt.user_id != current_user.id:
        abort(403)
    if current_attempt.completed_at:
        return redirect(url_for("student.result", attempt_id=attempt_id))
    if request.method == "POST":
        return _submit_attempt(current_attempt)
    return render_template("student/attempt.html", attempt=current_attempt)


def _submit_attempt(current_attempt):
    auto = request.form.get("auto_submit") == "1"
    total_points = 0
    max_total = 0
    for item in current_attempt.items:
        answer = request.form.get(f"answer_{item.id}", "").strip()
        item.student_answer = answer
        item.points = grade_answer(
            answer,
            item.correct_answer,
            item.question_type,
            current_attempt.grade_level,
            max_points=item.max_points,
        )
        item.is_correct = item.points >= item.max_points * 0.7
        total_points += item.points
        max_total += item.max_points
        _update_mastery(current_attempt.user_id, current_attempt.subject, current_attempt.grade_level,
                        current_attempt.semester, item.topic, item.is_correct)
    current_attempt.score = round(total_points / max_total * 100) if max_total else 0
    current_attempt.completed_at = datetime.now(timezone.utc)
    current_attempt.auto_submitted = auto
    db.session.commit()
    _refresh_recommended_courses(current_attempt.user_id)
    _mark_recommended_complete(current_attempt.user_id, current_attempt.subject, current_attempt.semester)
    return redirect(url_for("student.result", attempt_id=current_attempt.id))


def _update_mastery(user_id, subject, grade_level, semester, unit_name, is_correct):
    record = MasteryRecord.query.filter_by(
        user_id=user_id, subject=subject, grade_level=grade_level,
        semester=semester, unit_name=unit_name
    ).first()
    if not record:
        record = MasteryRecord(
            user_id=user_id, subject=subject, grade_level=grade_level,
            semester=semester, unit_name=unit_name
        )
        db.session.add(record)
    if is_correct:
        record.correct_answers += 1
    else:
        record.wrong_answers += 1
    record.last_attempt_at = datetime.now(timezone.utc)
    record.update_accuracy()


def _refresh_recommended_courses(user_id):
    """취약 단원을 기반으로 추천 학습 코스를 갱신합니다."""
    weak_records = MasteryRecord.query.filter_by(user_id=user_id).filter(
        MasteryRecord.accuracy_rate < 70
    ).order_by(MasteryRecord.accuracy_rate.asc(), MasteryRecord.updated_at.desc()).limit(10).all()

    # 기존 미완료 추천을 초기화하지 않고, 없는 것만 추가
    existing = {
        (r.subject, r.grade_level, r.semester, r.unit_name)
        for r in RecommendedCourse.query.filter_by(user_id=user_id, is_completed=False).all()
    }
    priority = 1
    for record in weak_records:
        key = (record.subject, record.grade_level, record.semester, record.unit_name)
        if key in existing:
            continue
        reason = f"{subject_name(record.subject)} {record.unit_name} 단원의 정답률이 {record.accuracy_rate}%입니다. 취약한 부분을 집중 복습해 보세요."
        course = RecommendedCourse(
            user_id=user_id,
            subject=record.subject,
            grade_level=record.grade_level,
            semester=record.semester,
            unit_name=record.unit_name,
            reason=reason,
            priority=priority,
        )
        db.session.add(course)
        priority += 1
    db.session.commit()


def _mark_recommended_complete(user_id, subject, semester):
    """해당 과목/학기의 추천 코스 중 정답률이 70% 이상이면 완료 처리합니다."""
    records = MasteryRecord.query.filter_by(
        user_id=user_id, subject=subject, semester=semester
    ).filter(MasteryRecord.accuracy_rate >= 70).all()
    unit_names = {r.unit_name for r in records}
    courses = RecommendedCourse.query.filter_by(
        user_id=user_id, subject=subject, semester=semester, is_completed=False
    ).filter(RecommendedCourse.unit_name.in_(unit_names)).all()
    now = datetime.now(timezone.utc)
    for course in courses:
        course.is_completed = True
        course.completed_at = now
    db.session.commit()


@student_bp.route("/recommended")
@login_required
def recommended_courses():
    """추천 학습 코스를 보여줍니다."""
    courses = (
        RecommendedCourse.query.filter_by(user_id=current_user.id, is_completed=False)
        .order_by(RecommendedCourse.priority.asc())
        .all()
    )
    return render_template("student/recommended.html", courses=courses)


@student_bp.route("/recommended/<int:course_id>/start")
@login_required
def start_recommended(course_id):
    """추천 코스의 단원을 집중 복습합니다."""
    course = db.get_or_404(RecommendedCourse, course_id)
    if course.user_id != current_user.id:
        abort(403)
    attempt = build_attempt(
        course.subject, count=10, semester=course.semester, focus_wrong=True
    )
    return redirect(url_for("student.attempt", attempt_id=attempt.id))

@student_bp.route("/result/<int:attempt_id>")
@login_required
def result(attempt_id):
    current_attempt = db.get_or_404(Attempt, attempt_id)
    if current_attempt.user_id != current_user.id or not current_attempt.completed_at:
        abort(403)
    return render_template("student/result.html", attempt=current_attempt)


@student_bp.route("/history")
@login_required
def history():
    attempts = (
        Attempt.query.filter_by(user_id=current_user.id)
        .filter(Attempt.completed_at.isnot(None))
        .order_by(Attempt.completed_at.desc())
        .all()
    )
    return render_template("student/history.html", attempts=attempts)


@student_bp.route("/wrong-answers")
@login_required
def wrong_answers():
    items = (
        AttemptItem.query.join(Attempt)
        .filter(Attempt.user_id == current_user.id, AttemptItem.is_correct.is_(False))
        .order_by(Attempt.completed_at.desc())
        .limit(100)
        .all()
    )
    return render_template("student/wrong_answers.html", items=items)


@student_bp.route("/english/memorize")
@login_required
def english_memorize():
    grade = current_user.grade_level
    sentences = SENTENCES.get(grade, SENTENCES[9])
    words = VOCABULARY.get(grade, VOCABULARY[9])
    word_images = {word: placeholder_image(word, width=100, height=100) for word, _ in words}
    return render_template(
        "student/english_memorize.html",
        sentences=sentences,
        words=words,
        word_images=word_images,
        grade=grade,
    )


@student_bp.route("/english/dictation", methods=["GET", "POST"])
@login_required
def english_dictation():
    grade = current_user.grade_level
    level = request.args.get("level", "elementary")
    category = request.args.get("category", "all")

    if request.method == "POST":
        answers = request.form.getlist("answer")
        correct = request.form.getlist("correct")
        items = []
        score = 0
        for ans, cor in zip(answers, correct):
            ok = is_correct(ans, cor)
            if ok:
                score += 1
            items.append({"answer": ans, "correct": cor, "is_correct": ok})
        total = len(correct) if correct else 1
        return render_template(
            "student/english_dictation_result.html",
            score=round(score / total * 100),
            items=items,
        )

    lessons = get_lessons()
    return render_template(
        "student/english_dictation.html",
        grade=grade,
        lessons=lessons,
        categories=CATEGORIES,
        levels=LEVELS,
        current_level=level,
        current_category=category,
    )