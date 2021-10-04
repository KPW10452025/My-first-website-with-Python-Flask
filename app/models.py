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
    avatar_img = db.Column(db.String(120), default="/static/asset/Default_avatar.JPG", nullable=False)
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
# >>> u1.followers                                                           # 查看 u1 被哪些人關注。u1 的粉絲、u1 的追隨者
# []                                                                         # 空
# >>> u1.followed                                                            # 查看 u1 關注了誰、追隨了誰
# []                                                                         # 空
# >>> u1.followers.append(u2)                                                # 使用 append() 讓 u1 增加一個追隨者 u2
# >>> u1.followers                                                           # 再次查看 u1 的追隨者、被誰關注
# [<User 'u2'>]                                                              # u1 被 u2 關注了
# >>> u2.followed                                                            # 查看 u2 追隨了誰、關注了誰
# [<User 'u1'>]                                                              # u2 關注了 u1
# 只在 u1 做 append() 修改，但可以發現 u2 的資料也發生了改變

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

    def follow(self, user):
        # 運用 is_following 判斷目標是否已關注，因為若已關注會 return True 故在此用 if not
        if not self.is_following(self):
            self.followed.append(user)
            # 若尚未關注，則會關注目標
    
    def unfollow(self, user):
        # is_following 判斷目標是否已關注，因為若已關注會 return True
        if self.is_following(self):
            self.followed.remove(user)
            # 若已關注，則取消關注
        
    def is_following(self, user):
        return self.followed.filter(association_table_follow.c.followed_id == user.id).count > 0
        # 目標功能：判斷目標用戶是否已關注。
        # 說明一：當目標用戶，已被關注時，畫面會顯示“已關注”並無法再次點選關注。
        # 說明二：當目標用戶，尚未關注時，畫面會顯示“未關注”並可以點選關注。
        # 從 User 本身所有的已關注對象中，尋找是否有與目標相同的資料，若擁有則會大於零。
        # 若大於零 return True ，則代表用戶本身的資料庫中已擁有目標用戶，即為已關注。
        # 若等於零 return False，則代表用戶本身的資料庫中並沒有目標用戶，即為尚未關注。

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return '<POST {}>'.format(self.body)
