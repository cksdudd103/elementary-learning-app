import re, requests

s = requests.Session()
r = s.get('http://127.0.0.1:5000/auth/login')
m = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.text)
csrf = m.group(1)
r = s.post('http://127.0.0.1:5000/auth/login', data={'identity':'testuser','password':'testpass123','csrf_token':csrf}, allow_redirects=False)
print('login', r.status_code)
r = s.get('http://127.0.0.1:5000/learn/english/review')
print('review', r.status_code, len(r.text))
print('words', r.text.count('vocab-card'))
print('conversations', r.text.count('conversation-card'))
print('word form action', 'english/word-check' in r.text)
print('sentences', r.text.count('review-card'))
# submit word check
m = re.search(r'name="csrf_token"[^\u003e]*value="([^"]+)"', r.text)
print('csrf2 found', bool(m))
if m:
    csrf2 = m.group(1)
    r2 = s.post('http://127.0.0.1:5000/learn/english/word-check', data={'csrf_token':csrf2, 'learned':['apple|사과','book|책']}, allow_redirects=False)
    print('word-check', r2.status_code, r2.headers.get('Location'))
