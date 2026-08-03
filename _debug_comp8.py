from app import create_app
from werkzeug.routing import Rule
app=create_app()
app.view_functions['comp_test'] = lambda: 'hello'
app.url_map.add(Rule('/learn/test123', endpoint='comp_test'))

c=app.test_client()
with c.session_transaction() as sess:
    sess['_user_id']='1'
    sess['_fresh']=True
r=c.get('/learn/test123')
print('test123', r.status_code, r.get_data(as_text=True))
