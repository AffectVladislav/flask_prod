from flask import Flask

from .extensions import db, migrate, login_manager
from .config import Config
from .routes.post import post
from .routes.user import user


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(user)
    app.register_blueprint(post)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
    return app
