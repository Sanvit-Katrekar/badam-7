# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_socketio import SocketIO
from flask_cors import CORS
from app.constants import Mode, CONFIGURATION_MODE

app = Flask(__name__, static_url_path='/static')

#Configuration of application, see configuration.py, choose one and uncomment.
if CONFIGURATION_MODE == Mode.PRODUCTION:
    app.config.from_object('app.configuration.ProductionConfig')
elif CONFIGURATION_MODE == Mode.DEVELOPMENT:
    app.config.from_object('app.configuration.DevelopmentConfig')

cors = CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins=["http://127.0.0.1:5001", "*"])

bs = Bootstrap(app) #flask-bootstrap
db = SQLAlchemy(app) #flask-sqlalchemy

admin = Admin(app)

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

from app.admin_auth import AuthModelView
from app.models import User

admin.add_view(AuthModelView(User, db.session))

from app import views, models

from app.utils import time_in_words

app.jinja_env.globals.update(time_in_words=time_in_words)
