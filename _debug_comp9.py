from app import create_app
from app.models import User
from app.student.routes import start_comprehensive

app = create_app()
with app.app_context():
    u = User.query.first()
    print("user", u)
    with app.test_request_context("/learn/comprehensive/start", method="GET"):
        if u:
            from flask_login import login_user
            login_user(u)
        try:
            r = start_comprehensive()
            print("ok", r.status_code, r.location)
        except Exception as e:
            import traceback
            traceback.print_exc()
