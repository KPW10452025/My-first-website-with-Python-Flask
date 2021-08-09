# 此文檔用來設定各種邏輯運算

# UserMixin 功能：用戶認證，需放在 class User()裡面才能發揮作用
from flask_login import UserMixin

# 因為要設定 database 裡面的 table 故從 app.py 載入 db 以讓下面 db.Model 能運作
from app import db

# 為了製作 login 的 API 故從 app.py 載入 login 以讓下面 @login 能運作
from app import login

import jwt
from flask import current_app

from datetime import datetime

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin): # class User(db.Model): 是 flask_sqlalchemy 默認語法
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False) # unique 獨特性，nullable 可為空
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref=db.backref('author', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username
    
    def generate_reset_password_token(self):
        return jwt.encode({"id": self.id}, current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def check_reset_password_token(token):
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return User.query.filter_by(id=data['id']).first()
        except:
            return 

# 使用 terminal 並把位置調整到這裡
# 輸入 python3 開啟 python3 模式
# 輸入 from models import db
# 這時 terminal 會出現警告，可以無視
# 輸入 db.create_all()
# 這時會出現一個名為 app.db 資料庫（設定內容在檔案 config.py 裡面的 SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'）
# 輸入 from models import User
# 輸入 User.query.all() 會得到 [] 因為現在沒有任何使用者資料

# 加入使用者資料
# 輸入 user = User(username = "Jack", password = "asd" ,email = "Jack@gmail.com") 隨意創建一個使用者
# 輸入 db.session.add(user) 必須步驟
# 輸入 db.session.commit() 必須步驟，類似存擋的動作
# 此時再次輸入 User.query.all() 會得到 [<User 'Jack'>]

# 查看使用者資料
# User.query.all()是一個數組
# 輸入 User.query.all()[0].username 可得到 'Jack'
# 輸入 User.query.all()[0].email 可得到 'example@gmail.com'

# 刪除全部使用者資料
# 輸入 User.query.delete()
# 此時再次輸入 User.query.all() 會得到 []
# 輸入 db.session.commit() 必須步驟，類似存擋的動作

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # body 正文、文章內容
    body = db.Column(db.String(500), nullable=False)
    # timestamp 發文時間 # db.DateTime 為資料庫默認語法 # default=datetime.utcnow 將發文時間默認為當前 UTC 時間的 date 和 time
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return '<POST {}>'.format(self.body)

# {{ 測試 table User 和 table Post 的關係是否建立成功 }}
# 開啟 Python Shell
# >>> from app.models import db
# >>> db.create_all()
# >>> from app.models import User, Post
# >>> u1 = User(username='Alen', password='12345678', email='alen@gmail.com')
# >>> u1.posts
# []
# >>> u1.posts.append(Post(body='test text 1'))
# >>> u1.posts
# [<POST test text 1>]
# >>> p2 = Post(body='test text 2')
# >>> u1.posts.append(p2)
# >>> p2.author
# <User 'Alen'>

# {{ 查詢使用者發過的 post }}
# 開啟 Python Shell
# >>> from app.models import User
# >>> user = User.query.filter_by(username='test0001').first()   # 查詢使用者 test0001
# >>> user.posts
# [<POST hi>, <POST I am test0001.>]                             # 使用者 test0001 發過的 post
