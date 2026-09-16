import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Attempt, AttemptItem, User, utcnow

PASSWORD = "test-password-123"


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def make_user(role, name, grade_level=4, pin="1234", parent_id=None):
    user = User(
        username=f"{name}-{role}",
        email=f"{name}-{role}@example.com",
        display_name=name,
        role=role,
        grade_level=grade_level,
        simple_pin=pin,
        parent_id=parent_id,
    )
    user.set_password(PASSWORD)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture()
def admin(app):
    return make_user("admin", "관리자")


@pytest.fixture()
def parent(app):
    return make_user("parent", "학부모")


@pytest.fixture()
def other_parent(app):
    return make_user("parent", "다른학부모")


@pytest.fixture()
def student(app):
    return make_user("student", "학생", grade_level=4)


@pytest.fixture()
def other_student(app):
    return make_user("student", "다른학생", grade_level=5)


@pytest.fixture()
def child(app, parent):
    return make_user("student", "자녀", grade_level=3, pin="5678", parent_id=parent.id)


@pytest.fixture()
def completed_attempt(app, student):
    attempt = Attempt(
        user_id=student.id,
        subject="math",
        grade_level=student.grade_level,
        semester=1,
        completed_at=utcnow(),
        score=80,
        question_count=2,
    )
    db.session.add(attempt)
    db.session.flush()
    db.session.add(
        AttemptItem(
            attempt_id=attempt.id,
            position=1,
            question_type="write",
            topic="덧셈",
            prompt="1 + 1 = ?",
            correct_answer="2",
            student_answer="2",
            is_correct=True,
            points=10,
        )
    )
    db.session.commit()
    return attempt


def login(client, identity, password=PASSWORD):
    return client.post(
        "/auth/login",
        data={"identity": identity, "password": password},
        follow_redirects=False,
    )


def login_student(client, display_name, grade_level, pin):
    return client.post(
        "/auth/login",
        data={
            "display_name": display_name,
            "grade_level": grade_level,
            "simple_pin": pin,
        },
        follow_redirects=False,
    )
