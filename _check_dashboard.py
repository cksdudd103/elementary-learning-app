import re, requests

s = requests.Session()
r = s.get('http://127.0.0.1:5000/auth/login')
m = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.text)
csrf = m.group(1) if m else ''
r = s.post('http://127.0.0.1:5000/auth/login', data={
    'identity': 'testuser',
    'password': 'testpass123',
    'csrf_token': csrf,
})
print('login status:', r.status_code, 'location:', r.headers.get('Location'))
r = s.get('http://127.0.0.1:5000/learn/')
print('dashboard status:', r.status_code)
for line in r.text.splitlines():
    if '랜덤 시작' in line or '종합 평가' in line or '수학 랜덤' in line or '영어 랜덤' in line or '국어 랜덤' in line or '사회 랜덤' in line or '랜덤 문항' in line:
        print(line.strip())
