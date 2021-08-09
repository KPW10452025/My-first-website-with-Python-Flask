#【Flask 教程】16 - Flask SQLAlchemy 中的一對多的表格關係數據庫
# https://youtu.be/LMXUk2APw8o
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#simple-relationships

# {{ 製作貼文表格 }}
# 到 froms.py 加入 class PostTweetForm(FlaskForm):......
# from wtforms import TextAreaField
# 回到 route.py 加入 from app.forms.py import PostTweetForm
# 並將 form = PostTweetForm() 放入 @app.route("/") 中，並且記得在 return 中加入 form = form
# 因為要開啟頁面寫入和傳輸功能，將 methods=["Get", "Post"] 放到 @app.route("/") 中
# 在 index.heml 中加入以下編碼，始 PostTweetForm 能出現在頁面上
# <div class="row">
#     <div class="col-md-6">
#         {% import 'bootstrap/wtf.html' as wtf %}
#         {{ wtf.quick_form(form) }}
#     </div>
# </div>

# {{ 製作儲存貼文的 table }}
# 到 models.py 新增 class Post(db.Model):

# {{ 將 User 和 Post 兩個 tabl3 聯繫起來 }}
# 目前有兩個 table 但之間並無聯繫。實際狀況是，一個 user 會有很多 post，但一個 post 只會有一個 user
# 所以在 Post 中就要儲存一個 foreign_key，而這個 foreign_key 就是 User 的 id
# 在 table User 中新增 posts = db.relationship('Post', backref=db.backref('author', lazy=True))
# 在 table Post 中寫入 user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 到 route.py 的 @app.route("/", methods=["Get", "Post"]) 裡面的 if form.validate_on_submit():

from flask import Flask # Flask 網頁開發主要功能  # render_template 載入 HTML 文檔的工具
from flask_bootstrap import Bootstrap # Bootstrap 美化頁面工具
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy 資料庫相關
from flask_bcrypt import Bcrypt # 加密文件用的 package 
from flask_login import LoginManager # 製作 flask login API
from flask_mail import Mail # 開啟網頁寄信功能

from config import Config # 把 config 另外放到其他檔案時，默認需要編碼

import ssl 
ssl._create_default_https_context = ssl._create_unverified_context
# 20210728註記：據我目前能力所知，需要回傳數據到 mac 電腦時，需要本地認證書 local issuer certificate
# 此代碼能解決無認證書的問題
# 實際用法尚不知

app = Flask(__name__) # Flask 默認語法
app.config.from_object(Config)# 把 config 另外放到其他檔案時，默認需要編碼
# https://dormousehole.readthedocs.io/en/latest/config.html
# 在文檔中有提到
# 如果要使用專門的 config.py 配置文件
# ==================================================
# class Config(object):
#     TESTING = False
# class ProductionConfig(Config):
#     DATABASE_URI = 'mysql://user@localhost/foo'
# class DevelopmentConfig(Config):
#     DATABASE_URI = "sqlite:////tmp/foo.db"
# class TestingConfig(Config):
#     DATABASE_URI = 'sqlite:///:memory:'
#     TESTING = True
# ==================================================
# 那必須在主文件中使用以下語法
# from config import Config
# app.config.from_object(Config)

bootstrap = Bootstrap(app) # flask_bootstrap 默認語法
db = SQLAlchemy(app) # flask_sqlalchemy 默認語法
bcrypt = Bcrypt(app) # flask_bcrypt 默認語法
login = LoginManager(app) # flask_login 默認語法
mail = Mail(app) # flask_mail 默認語法

login.login_view = "login" # 設定登入者介面位置
login.login_message = "You must login to access 「HOME 主頁」"
login.login_message_category = "warning"

from app.route import * # 單純為防止 python circular import 而做的 import
