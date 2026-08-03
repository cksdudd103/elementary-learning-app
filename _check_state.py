from app import create_app
from app.extensions import db
from app.models import Attempt

app = create_app()
with app.app_context():
    cols = [c.name for c in db.inspect(Attempt).columns]
    print('Attempt columns:', cols)
    ctx = app.test_request_context()
    ctx.push()
    ctx_data = app.make_shell_context()
    print('random_count in shell ctx:', 'random_count' in ctx_data)
    ctx.pop()
