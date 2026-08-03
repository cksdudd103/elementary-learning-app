from app import create_app
import re
app=create_app()
c=app.test_client()
r=c.get('/auth/login')
t=r.get_data(as_text=True)
lines=[l.strip() for l in t.split('\n') if 'csrf_token' in l]
m=re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', lines[0])
csf=m.group(1)
r_login = c.post('/auth/login',data={'identity':'testuser','password':'testpass123','csrf_token':csf})
print('login post status', r_login.status_code, 'loc', r_login.headers.get('Location'))

r=c.get('/learn/comprehensive/start')
print('comp', r.status_code, r.headers.get('Location'))

# user agent가 없어서? accept?
r2=c.get('/learn/comprehensive/start', headers={'Accept':'text/html,application/xhtml+xml'})
print('comp2', r2.status_code, r2.headers.get('Location'))

r3=c.get('/learn/math/start')
print('math', r3.status_code, r3.headers.get('Location'))
