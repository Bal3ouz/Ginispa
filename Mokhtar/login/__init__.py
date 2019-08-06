from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache


app = Flask(__name__)
app.config['SECRET_KEY'] = '6673ffee83188cb99b4acff21ef56e03'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

cache.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from login import routes
#import routes