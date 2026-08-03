from app import create_app
from app.models import User
from app.student.routes import start_math, start_english, start_korean, start_social, start_comprehensive

app = create_app()
with app.app_context():
    u = User.query.first()
    with app.test_request_context(method="GET"):
        from flask_login import login_user
        login_user(u)
        for name, fn, count, subj in [
            ("math30", start_math, "30", "math"),
            ("english20", start_english, "20", "english"),
            ("korean10", start_korean, "10", "korean"),
            ("social30", start_social, "30", "social"),
            ("comprehensive", start_comprehensive, None, "comprehensive"),
        ]:
            with app.test_request_context(f"/learn/{subj}/start?count={count}" if count else "/learn/comprehensive/start", method="GET"):
                try:
                    if subj == "comprehensive":
                        r = fn()
                    else:
                        r = fn()
                    print(name, r.status_code, r.location)
                except Exception as e:
                    import traceback
                    print(name, "ERROR")
                    traceback.print_exc()
