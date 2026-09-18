"""권한별 접근 제어 테스트.

역할(비로그인/학생/학부모/관리자)별로 허용된 페이지에만 접근할 수 있는지,
다른 사용자의 리소스에는 접근할 수 없는지 검증한다.
"""

from tests.conftest import login, login_student, PASSWORD

ADMIN_PAGES = [
    "/admin/",
    "/admin/students",
    "/admin/questions",
    "/admin/questions/new",
    "/admin/curriculum-units",
    "/admin/curriculum-units/new",
    "/admin/education-offices",
    "/admin/schools",
]

STUDENT_PAGES = [
    "/learn/",
    "/learn/history",
    "/learn/wrong-answers",
    "/learn/recommended",
    "/learn/english/dictation",
]


# ---------------------------------------------------------------------------
# 비로그인 사용자
# ---------------------------------------------------------------------------

def test_anonymous_redirected_to_login(client):
    for path in ADMIN_PAGES + ["/parent/"] + STUDENT_PAGES:
        res = client.get(path)
        assert res.status_code == 302, f"{path} should redirect"
        assert res.headers["Location"].startswith("/auth/login"), f"{path} -> {res.headers['Location']}"


def test_anonymous_can_view_public_pages(client):
    for path in ["/", "/auth/login", "/auth/register/student", "/auth/register/parent", "/auth/forgot-password"]:
        assert client.get(path).status_code == 200, path


# ---------------------------------------------------------------------------
# 학생
# ---------------------------------------------------------------------------

def test_student_can_access_student_pages(client, student):
    login(client, student.username)
    for path in STUDENT_PAGES:
        assert client.get(path).status_code == 200, path


def test_student_forbidden_on_admin_pages(client, student):
    login(client, student.username)
    for path in ADMIN_PAGES:
        assert client.get(path).status_code == 403, path


def test_student_forbidden_on_parent_pages(client, student):
    login(client, student.username)
    assert client.get("/parent/").status_code == 403


def test_student_cannot_view_others_attempt(client, student, other_student, completed_attempt):
    login(client, other_student.username)
    assert client.get(f"/learn/attempt/{completed_attempt.id}").status_code == 403


def test_student_cannot_view_others_result(client, other_student, completed_attempt):
    login(client, other_student.username)
    assert client.get(f"/learn/result/{completed_attempt.id}").status_code == 403


def test_student_can_view_own_result(client, student, completed_attempt):
    login(client, student.username)
    assert client.get(f"/learn/result/{completed_attempt.id}").status_code == 200


def test_student_cannot_start_others_recommended_course(client, other_student, student):
    from app.extensions import db
    from app.models import RecommendedCourse

    course = RecommendedCourse(
        user_id=student.id,
        subject="math",
        grade_level=student.grade_level,
        semester=1,
        unit_name="덧셈과 뺄셈",
        reason="정답률 미달",
        priority=1,
    )
    db.session.add(course)
    db.session.commit()

    login(client, other_student.username)
    assert client.get(f"/learn/recommended/{course.id}/start").status_code == 403


# ---------------------------------------------------------------------------
# 학부모
# ---------------------------------------------------------------------------

def test_parent_can_access_parent_dashboard(client, parent):
    login(client, parent.username)
    assert client.get("/parent/").status_code == 200


def test_parent_forbidden_on_admin_pages(client, parent):
    login(client, parent.username)
    for path in ADMIN_PAGES:
        assert client.get(path).status_code == 403, path


def test_parent_redirected_from_student_pages(client, parent):
    login(client, parent.username)
    for path in STUDENT_PAGES:
        res = client.get(path)
        assert res.status_code == 302, path
        assert res.headers["Location"].startswith("/parent/")


def test_parent_can_view_own_child(client, parent, child):
    login(client, parent.username)
    assert client.get(f"/parent/children/{child.id}").status_code == 200


def test_parent_cannot_view_other_parents_child(client, other_parent, child):
    login(client, other_parent.username)
    assert client.get(f"/parent/children/{child.id}").status_code == 403


def test_parent_cannot_view_unlinked_student(client, parent, student):
    login(client, parent.username)
    assert client.get(f"/parent/children/{student.id}").status_code == 403


def test_parent_cannot_view_other_parents_child_attempt(client, other_parent, child, completed_attempt):
    login(client, other_parent.username)
    res = client.get(f"/parent/children/{child.id}/attempt/{completed_attempt.id}")
    assert res.status_code == 403


def test_parent_cannot_reset_other_parents_child_password(client, other_parent, child):
    login(client, other_parent.username)
    assert client.get(f"/parent/children/{child.id}/reset-password").status_code == 403


def test_parent_dashboard_grade_filter(client, parent, child):
    from app.extensions import db
    from app.models import User

    # Create another child in a different grade
    child2 = User(
        username="child2",
        email="child2@example.com",
        display_name="둘째",
        role="student",
        grade_level=5,
        simple_pin="1234",
        parent_id=parent.id,
    )
    child2.set_password("testpass")
    db.session.add(child2)
    db.session.commit()

    login(client, parent.username)

    res = client.get("/parent/")
    assert res.status_code == 200
    assert f"/parent/children/{child.id}".encode() in res.data
    assert f"/parent/children/{child2.id}".encode() in res.data

    res = client.get("/parent/?grade=3")
    assert res.status_code == 200
    assert f"/parent/children/{child.id}".encode() in res.data
    assert f"/parent/children/{child2.id}".encode() not in res.data

    res = client.get("/parent/?grade=5")
    assert res.status_code == 200
    assert f"/parent/children/{child.id}".encode() not in res.data
    assert f"/parent/children/{child2.id}".encode() in res.data


# ---------------------------------------------------------------------------
# 관리자
# ---------------------------------------------------------------------------

def test_admin_can_access_admin_pages(client, admin):
    login(client, admin.username)
    for path in ADMIN_PAGES:
        assert client.get(path).status_code == 200, path


def test_admin_forbidden_on_parent_pages(client, admin):
    login(client, admin.username)
    assert client.get("/parent/").status_code == 403


def test_admin_redirected_from_student_pages(client, admin):
    login(client, admin.username)
    res = client.get("/learn/")
    assert res.status_code == 302
    assert res.headers["Location"].startswith("/parent/")


# ---------------------------------------------------------------------------
# 로그인 라우팅
# ---------------------------------------------------------------------------

def test_admin_login_redirects_to_admin_dashboard(client, admin):
    res = login(client, admin.username)
    assert res.status_code == 302
    assert res.headers["Location"].startswith("/admin/")


def test_student_login_redirects_to_student_dashboard(client, student):
    res = login(client, student.username)
    assert res.status_code == 302
    assert res.headers["Location"].startswith("/learn/")


def test_student_pin_login(client, student):
    res = login_student(client, student.display_name, student.grade_level, "1234")
    assert res.status_code == 302
    assert res.headers["Location"].startswith("/learn/")
    assert client.get("/learn/").status_code == 200


def test_student_pin_login_with_wrong_pin(client, student):
    res = login_student(client, student.display_name, student.grade_level, "9999")
    assert res.status_code == 200  # 오류 메시지와 함께 폼 재표시
    assert "이름, 학년, PIN을 확인하세요" in res.get_data(as_text=True)


def test_login_with_wrong_password(client, student):
    res = login(client, student.username, "wrong-password")
    assert res.status_code == 200
    assert "아이디 또는 비밀번호를 확인하세요" in res.get_data(as_text=True)


# ---------------------------------------------------------------------------
# 관리자 계정 관리
# ---------------------------------------------------------------------------

def test_admin_can_access_users_page(client, admin):
    login(client, admin.username)
    assert client.get("/admin/users").status_code == 200


def test_admin_delete_user_removes_account(client, admin, student, completed_attempt):
    student_id = student.id
    login(client, admin.username)
    res = client.post(f"/admin/users/{student_id}/delete", follow_redirects=True)
    assert res.status_code == 200
    from app.models import Attempt, User

    assert User.query.get(student_id) is None
    assert Attempt.query.filter_by(user_id=student_id).count() == 0


def test_admin_cannot_delete_admin_account(client, admin):
    from app.extensions import db
    from app.models import User

    other_admin = User(
        username="other-admin",
        email="other-admin@example.com",
        display_name="다른관리자",
        role="admin",
        grade_level=1,
    )
    other_admin.set_password(PASSWORD)
    db.session.add(other_admin)
    db.session.commit()

    login(client, admin.username)
    res = client.post(f"/admin/users/{other_admin.id}/delete", follow_redirects=True)
    assert res.status_code == 200
    assert "관리자 계정은 삭제할 수 없습니다" in res.get_data(as_text=True)
    assert User.query.get(other_admin.id) is not None


def test_admin_users_reset_keeps_admin_only(client, admin, student, parent, child):
    removed_ids = {student.id, parent.id, child.id}
    login(client, admin.username)
    res = client.post("/admin/users/reset", follow_redirects=True)
    assert res.status_code == 200
    assert "3개를 초기화했습니다" in res.get_data(as_text=True)

    from app.models import User

    remaining = User.query.all()
    remaining_ids = {u.id for u in remaining}
    assert all(u.role == "admin" for u in remaining)
    assert admin.id in remaining_ids
    assert removed_ids.isdisjoint(remaining_ids)


def test_student_forbidden_on_users_reset(client, student):
    login(client, student.username)
    assert client.post("/admin/users/reset").status_code == 403
    assert client.post(f"/admin/users/{student.id}/delete").status_code == 403


def test_parent_forbidden_on_user_delete(client, parent, student):
    login(client, parent.username)
    assert client.post(f"/admin/users/{student.id}/delete").status_code == 403
