import os

from flask_migrate import Migrate

from app import db, create_app
from app.models import User, Post, Role


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Role': Role}

