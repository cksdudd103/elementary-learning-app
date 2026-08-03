from app import create_app
import re
app=create_app()
c=app.test_client()
r = c.get('/auth/login')
text = r.get_data(as_text=True)
m = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', text)
csf = m.group(1)
r = c.post('/auth/login', data={'identity':'testuser','password':'testpass123','csrf_token':csf})
print('login', r.status_code)
r = c.get('/learn/english/review')
print('review', r.status_code, len(r.get_data(as_text=True)))
print(r.get_data(as_text=True)[:1000])
