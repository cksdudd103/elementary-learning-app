from app import create_app
import re
app=create_app()
c=app.test_client()
r=c.get('/auth/login')
t=r.get_data(as_text=True)
lines=[l.strip() for l in t.split('\n') if 'csrf_token' in l]
print('line', lines[0])
m=re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', lines[0])
print('m', m)
