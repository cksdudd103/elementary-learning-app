import re, requests

s = requests.Session()
r = s.get('http://127.0.0.1:5000/auth/login')
m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text)
csrf = m.group(1)
r = s.post('http://127.0.0.1:5000/auth/login', data={'identity':'testuser','password':'testpass123','csrf_token':csrf}, allow_redirects=False)
print('login', r.status_code)
r = s.get('http://127.0.0.1:5000/learn/comprehensive/start', allow_redirects=False)
print('comprehensive', r.status_code, r.headers.get('Location'))
if r.status_code == 302:
    loc = r.headers['Location']
    r2 = s.get('http://127.0.0.1:5000' + loc)
    print('attempt', r2.status_code, len(r2.text))
    print('question count', r2.text.count('question-card'))
