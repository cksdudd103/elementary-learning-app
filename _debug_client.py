from app import create_app

app = create_app()
rules = [(str(r), r.endpoint) for r in app.url_map.iter_rules()]
for rule, endpoint in sorted(rules):
    if 'comprehensive' in rule or 'start' in rule:
        print(rule, endpoint)

with app.test_client() as client:
    r = client.get('/learn/comprehensive/start')
    print('no auth status', r.status_code)
    print(r.headers.get('Location'))
