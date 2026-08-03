import requests, re

s = requests.Session()
r = s.get('http://127.0.0.1:5000/auth/login')
csrf = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.text).group(1)
s.post('http://127.0.0.1:5000/auth/login', data={'identity':'testuser','password':'testpass123','csrf_token':csrf}, allow_redirects=False)
r = s.get('http://127.0.0.1:5000/learn/comprehensive/start', allow_redirects=False)
print('status', r.status_code)
print('headers', dict(r.headers))
print('body preview', r.text[:200])
