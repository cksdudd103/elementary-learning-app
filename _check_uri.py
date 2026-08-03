from app import create_app
from app.extensions import db

app = create_app()
print('SQLALCHEMY_DATABASE_URI:', app.config['SQLALCHEMY_DATABASE_URI'])
with app.app_context():
    print('Attempt columns:', [c.name for c in db.inspect(db.Model.metadata.tables['attempt']).columns])
