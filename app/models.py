from flask_login import UserMixin
from app import db
from app import login
import jwt
from flask import current_app

from datetime import datetime

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# 關聯表，左側的 user 正在關注右側的 user
association_table_follow = db.Table("association_table_follow",
            db.Column("follower_id", db.Integer, db.ForeignKey("user.id")), # 左側
            db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))  # 右側
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref=db.backref('author', lazy=True))
    # 建立好 association_table_follow 這個 Table 後，需要把 association_table_follow 和 User 做聯接，故須在這邊添加 relationship
    followed = db.relationship(
        # 從 User 要往誰去連？要連去另一個 User 所以下面也是 "User"
        "User", secondary=association_table_follow,
        primaryjoin=(association_table_follow.c.follower_id == id),
        secondaryjoin=(association_table_follow.c.followed_id == id),
        backref=db.backref('followers', lazy=True), lazy=True
    )

# 到 python3 shell 進行測試：讓 u1 追隨 u2
# >>> from app.models import db
# >>> db.create_all()                                                        # 更新資料庫結構
# >>> from app.models import User
# >>> u1 = User(username='u0001', password='12341234', email='u1@gmail.com') # 新建測試用 u1
# >>> u2 = User(username='u0002', password='12341234', email='u2@gmail.com') # 新建測試用 u2
# >>> u1.followers                                                           # 查看 u1 追隨哪些人
# []                                                                         # 空
# >>> u1.followed                                                            # 查看 u1 被誰追隨
# []                                                                         # 空
# >>> u1.followers.append(u2)                                                # 使用 append() 讓 u1 追隨 u2 
# >>> u1.followers                                                           # 再次查看 u1 追隨哪些人
# [<User 'u2'>]                                                              # u1 追隨了 u2
# >>> u2.followed                                                            # 查看 u2 被誰追隨
# [<User 'u1'>]                                                              # u2 被 u1 追隨
# 只在 u1 做 append() 修改，但可以發現 u2 的資料也發生了改變

# 測試：u2 不想被 u1 追隨。亦即 u2 取消 u1 的追隨
# >>> u2.followed.remove(u1)                                              # 使用 remove 讓 u2 取消 u1 的追隨                         
# >>> u2.followed                                                         # 再次觀看 u2 被哪些人追隨
# []                                                                      # 空
# >>> u1.followers                                                        # 此時因為資料庫的連動，觀看 u1 追隨哪些人
# []                                                                      # 空

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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return '<POST {}>'.format(self.body)
