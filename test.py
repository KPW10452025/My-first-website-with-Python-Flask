from app.models import db, User
from app import app

user = User.query.all()[0]
print(user)
# <User 'test0001'>

# 進行加密，並且另加密訊息 = key999
with app.app_context():
    key999 = user.generate_reset_password_token()

# 進行解密
with app.app_context():
    print(user.check_reset_password_token(key999))
# <User 'test0001'>
