from app import create_app
import re
app=create_app()
c=app.test_client()
r=c.get('/auth/login')
t=r.get_data(as_text=True)
lines=[l.strip() for l in t.split('\n') if 'csrf_token' in l]
m=re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', lines[0])
csf=m.group(1)
c.post('/auth/login',data={'identity':'testuser','password':'testpass123','csrf_token':csf})

# url adapter 직접
with c.session_transaction() as sess:
    print('session keys', list(sess.keys()))

r=c.get('/learn/comprehensive/start')
print('comp', r.status_code, r.headers.get('Location'))
print('data', r.get_data(as_text=True)[:200])
