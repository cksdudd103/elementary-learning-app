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

for subject in ['math', 'english', 'korean', 'social']:
    for count in [10, 20, 30]:
        r = s.get(f'http://127.0.0.1:5000/learn/{subject}/start?count={count}', allow_redirects=False)
        if r.status_code != 302:
            print(subject, count, 'FAIL', r.status_code)
            print(r.text[:500])
        else:
            loc = r.headers['Location']
            if loc.startswith('/'):
                loc = 'http://127.0.0.1:5000' + loc
            r2 = s.get(loc)
            print(subject, count, 'OK', r2.status_code, 'len', len(r2.text))
