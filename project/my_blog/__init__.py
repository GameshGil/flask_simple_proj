"""Initialize Flask app"""
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect


migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()


def create_app():
    """Construct core Flask app."""
    app = Flask(__name__, instance_relative_config=False)

    config_filename = 'config.Config'
    app.config.from_object(config_filename)

    from my_blog.models import db
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    csrf.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from my_blog import routes

        return app
