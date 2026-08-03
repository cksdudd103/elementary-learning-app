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

r = s.get('http://127.0.0.1:5000/learn/math/start?count=10', allow_redirects=False)
loc = r.headers['Location']
if loc.startswith('/'):
    loc = 'http://127.0.0.1:5000' + loc
r = s.get(loc)
print('attempt status', r.status_code)

form_data = {'csrf_token': csrf, 'auto_submit': '0'}
for i in range(1, 11):
    form_data[f'answer_{i}'] = '1'
r = s.post(loc, data=form_data, allow_redirects=False)
print('submit status', r.status_code, 'location', r.headers.get('Location'))
if r.status_code != 302:
    print(r.text[:1500])
else:
    loc2 = r.headers['Location']
    if loc2.startswith('/'):
        loc2 = 'http://127.0.0.1:5000' + loc2
    r2 = s.get(loc2)
    print('result status', r2.status_code)
    print('result contains score:', '점' in r2.text or 'score' in r2.text)
