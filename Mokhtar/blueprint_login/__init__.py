from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from blueprint_login.config import Config
from flask_caching import Cache


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
cache = Cache(config={'CACHE_TYPE': 'simple'})
mail=Mail()
#app.config['SECRET_KEY'] = '6673ffee83188cb99b4acff21ef56e03'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    cache.init_app(app)
    mail.init_app(app)

    from blueprint_login.users.routes import users
    from blueprint_login.main.routes import main
    from blueprint_login.feedback.routes import feedback
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(feedback)

    return app
