from app import create_app
from app.models import User
from app.student.routes import start_math

app = create_app()
with app.app_context():
    u = User.query.first()
    with app.test_request_context("/learn/math/start?count=20", method="GET"):
        from flask_login import login_user
        login_user(u)
        try:
            r = start_math()
            print("ok", r.status_code, r.location)
        except Exception as e:
            import traceback
            traceback.print_exc()
