import requests, re

s = requests.Session()
r = s.get('http://127.0.0.1:5000/auth/login')
m = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.text)
csf = m.group(1)
r = s.post('http://127.0.0.1:5000/auth/login', data={'identity':'testuser','password':'testpass123','csrf_token':csf}, allow_redirects=False)
print('login', r.status_code, r.headers.get('Location'))
r = s.get('http://127.0.0.1:5000/learn/english/review')
print('review', r.status_code, len(r.text))
print(r.text[:3000])
