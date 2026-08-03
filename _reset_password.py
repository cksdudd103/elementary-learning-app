from app import create_app
from app.models import User
from app.extensions import db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    u = User.query.filter_by(email="test@example.com").first()
    if u:
        u.password_hash = generate_password_hash("testpass1234")
        db.session.commit()
        print("password reset done")
    else:
        print("user not found")
