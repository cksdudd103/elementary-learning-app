import re, requests

s = requests.Session()
r = s.get('http://127.0.0.1:5000/auth/login')
m = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.text)
csrf = m.group(1) if m else ''
s.post('http://127.0.0.1:5000/auth/login', data={
    'identity': 'testuser',
    'password': 'testpass123',
    'csrf_token': csrf,
}, allow_redirects=False)
s.post('http://127.0.0.1:5000/learn/settings', data={'csrf_token': csrf, 'grade_level': '1'}, allow_redirects=False)

for _ in range(20):
    r = s.get('http://127.0.0.1:5000/learn/math/start?count=10', allow_redirects=False)
    loc = r.headers['Location']
    if loc.startswith('/'):
        loc = 'http://127.0.0.1:5000' + loc
    r2 = s.get(loc)
    if 'data:image/svg+xml' in r2.text:
        for line in r2.text.splitlines():
            if 'data:image/svg+xml' in line or 'IMG|' in line or '사과' in line:
                print(line.strip()[:300])
        break
else:
    print('no image option found')
