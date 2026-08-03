from app import create_app
import re
app=create_app()
c=app.test_client()
r=c.get('/auth/login')
t=r.get_data(as_text=True)
line=[l for l in t.split('\n') if 'csrf_token' in l][0]
print(repr(line))
m=re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', line)
print('m', m)
if m:
    csf=m.group(1)
    c.post('/auth/login',data={'identity':'testuser','password':'testpass123','csrf_token':csf})
    r=c.get('/learn/comprehensive/start')
    print('comp', r.status_code, r.headers.get('Location'))
