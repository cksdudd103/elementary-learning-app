from app import create_app
from app.models import User
from werkzeug.security import check_password_hash
app=create_app()
with app.app_context():
    u = User.query.filter_by(username='testuser').first()
    print(u, u.check_password('testpass123'))
    print('role', u.role, 'grade', u.grade_level)
