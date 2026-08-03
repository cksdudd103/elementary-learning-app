from app import create_app
import re
app=create_app()

# login_user 직접
from flask_login import login_user
from app.models import User
with app.app_context():
    user = User.query.filter_by(username='testuser').first()
    print('user', user)

c=app.test_client()
with c.session_transaction() as sess:
    sess['_user_id'] = str(user.id)
    sess['_fresh'] = True

r=c.get('/learn/comprehensive/start')
print('comp', r.status_code, r.headers.get('Location'))

r=c.get('/learn/')
print('dash', r.status_code)
