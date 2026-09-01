import json
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    grade_level = db.Column(db.Integer, nullable=False, default=1)
    ui_language = db.Column(db.String(2), nullable=False, default="ko")
    time_limit_seconds = db.Column(db.Integer, nullable=False, default=3600)
    difficulty = db.Column(db.String(10), nullable=False, default="medium")
    reset_token = db.Column(db.String(120), unique=True, nullable=True, index=True)
    reset_token_expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)

    children = db.relationship(
        "User", backref=db.backref("parent", remote_side=[id]), cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_parent(self):
        return self.role == "parent"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(20), nullable=False, index=True)
    grade_level = db.Column(db.Integer, nullable=False, index=True)
    topic = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False, default=1)
    question_type = db.Column(db.String(20), nullable=False, default="write")
    prompt = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text)
    answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False, default="")
    source = db.Column(db.String(20), nullable=False, default="admin")
    active = db.Column(db.Boolean, nullable=False, default=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)

    @property
    def options(self):
        return json.loads(self.options_json) if self.options_json else []

    @options.setter
    def options(self, value):
        self.options_json = json.dumps(value, ensure_ascii=False) if value else None


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    subject = db.Column(db.String(20), nullable=False)
    grade_level = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    completed_at = db.Column(db.DateTime(timezone=True))
    score = db.Column(db.Integer)
    time_limit_seconds = db.Column(db.Integer, nullable=False, default=3600)
    question_count = db.Column(db.Integer, nullable=False, default=10)
    is_comprehensive = db.Column(db.Boolean, nullable=False, default=False)
    auto_submitted = db.Column(db.Boolean, nullable=False, default=False)
    user = db.relationship(
        "User", backref=db.backref("attempts", lazy=True, cascade="all, delete-orphan")
    )
    items = db.relationship(
        "AttemptItem", backref="attempt", cascade="all, delete-orphan", order_by="AttemptItem.position"
    )


class AttemptItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey("attempt.id"), nullable=False, index=True)
    position = db.Column(db.Integer, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    topic = db.Column(db.String(80), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text)
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False, default="")
    student_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)
    points = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    max_points = db.Column(db.Integer, nullable=False, default=10)

    @property
    def options(self):
        return json.loads(self.options_json) if self.options_json else []

    @options.setter
    def options(self, value):
        self.options_json = json.dumps(value, ensure_ascii=False) if value else None


class EducationOffice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(40))
    homepage = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)

    schools = db.relationship("School", backref="education_office", lazy=True)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    education_office_id = db.Column(db.Integer, db.ForeignKey("education_office.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    school_type = db.Column(db.String(20), nullable=False)  # elementary, middle, high
    address = db.Column(db.String(255))
    phone = db.Column(db.String(40))
    homepage = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)


class CurriculumUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(20), nullable=False, index=True)
    grade_level = db.Column(db.Integer, nullable=False, index=True)
    unit_order = db.Column(db.Integer, nullable=False, default=1)
    unit_name = db.Column(db.String(120), nullable=False)
    learning_objective = db.Column(db.Text)
    keywords = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)