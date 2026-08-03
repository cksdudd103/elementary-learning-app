from app import create_app
app=create_app()
c=app.test_client()
with c.session_transaction() as sess:
    sess['_user_id']='1'
    sess['_fresh']=True
r=c.get('/learn/comprehensive/start')
print('FlaskClient comp', r.status_code, r.headers.get('Location'))

# app wsgi_app 직접 호출
from io import BytesIO
def start_response(status, headers):
    print('WSGI status', status, 'headers', headers)

environ = c.get('/').environ if hasattr(c.get('/'), 'environ') else {}
print('environ sample', environ.get('REQUEST_METHOD'))

# c.environ_base?
print('environ_base', c.environ_base)
