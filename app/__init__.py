from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
mail = Mail(app)

login.login_view = "login"
login.login_message = "You must login to access 「HOME 主頁」"
login.login_message_category = "warning"

from app.route import *
