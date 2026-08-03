import re, requests

s = requests.Session()
r = s.get('http://127.0.0.1:5000/auth/login')
m = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.text)
csrf = m.group(1) if m else ''
r = s.post('http://127.0.0.1:5000/auth/login', data={
    'identity': 'testuser',
    'password': 'testpass123',
    'csrf_token': csrf,
}, allow_redirects=False)
print('login', r.status_code, 'cookies', s.cookies.get_dict())
r = s.get('http://127.0.0.1:5000/learn/comprehensive/start', allow_redirects=False)
print('comprehensive', r.status_code, r.headers.get('Location'))
print('response cookies', r.headers.get('Set-Cookie'))
if r.status_code != 302:
    print(r.text[:1500])
else:
    loc = r.headers['Location']
    if loc.startswith('/'):
        loc = 'http://127.0.0.1:5000' + loc
    r2 = s.get(loc)
    print('attempt', r2.status_code)
    if r2.status_code != 200:
        print(r2.text[:1500])
    else:
        print('ok length', len(r2.text))
