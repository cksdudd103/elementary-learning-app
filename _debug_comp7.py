from app import create_app
app=create_app()
c=app.test_client()
with c.session_transaction() as sess:
    sess['_user_id']='1'
    sess['_fresh']=True
r=c.get('/learn/comprehensive/start')
print('request', r.request)
print('request path', r.request.path if r.request else None)
print('request url', r.request.url if r.request else None)
print('response status', r.status_code)

r2=c.get('/learn/math/start')
print('math request path', r2.request.path if r2.request else None)
print('math status', r2.status_code, r2.headers.get('Location'))
