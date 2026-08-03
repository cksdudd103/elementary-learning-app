from app import create_app
import re
app=create_app()
c=app.test_client()
r=c.get('/auth/login')
m=re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.get_data(as_text=True))
c.post('/auth/login',data={'identity':'testuser','password':'testpass123','csrf_token':m.group(1)})
r=c.get('/learn/english/review')
t=r.get_data(as_text=True)
print('len', len(t))
print('vocab', t.count('vocab-card'))
print('conversation', t.count('conversation-card'))
idx = t.find('vocab-card')
print(t[idx:idx+800])
