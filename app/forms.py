# 這個檔案會建立 register 頁面的各種邏輯運算

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User

# 現在要做名為 RegisterForm 的註冊單表，語法 class 名稱(FlaskForm)
class RegisterForm(FlaskForm):
    username = StringField('Username 請輸入使用者名稱', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email 請輸入信箱', validators=[DataRequired(), Email()])
    password = PasswordField('Password 請輸入密碼', validators=[DataRequired(), Length(min=8, max=20)])
    comfirm = PasswordField('Repeat Password 請再次輸入密碼已確認', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('OK and Register 確認並提交')


    # 語法 validate_要檢查項目的名稱
    # 比方說今天要檢查 username 所以就是 validate_username
    def validate_username(self, username):
        # 先用 query 和 filter_by 搜尋並塞選資料庫，尋找是否有合乎 username 的資料
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already registered. 此用戶名已被註冊。')
    # 檢查 email 如法炮製
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is already registered. 此信箱已被註冊。')


# 使用 flask_wtf 默認要搭配 SECRET_KEY
# 故要去 config 設定 SECRET_KEY

# wtforms.validators 包含各種驗證器，在驗證表單域時非常有用。以下列表顯示了常用的驗證器
# DataRequired 檢查輸入欄是否爲空
# Email 檢查字段中的文本是否遵循電子郵件ID約定
# IPAddress 驗證輸入字段中的IP地址
# Length 驗證輸入字段中字符串的長度是否在給定範圍內 Length(min=最小字數, max=最大字數)
# NumberRange 在給定範圍內的輸入字段中驗證一個數字
# URL 驗證輸入字段中輸入的URL

# 現在要製作 login 頁面的填寫表單
# 在上方有新增一個 from wtforms import ...... BooleanField
class LoginForm(FlaskForm):
    username = StringField('Username 請輸入使用者名稱', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password 請輸入密碼', validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField('Remenber')
    submit = SubmitField('Sign In 登入')

class PasswordResetRequestForm(FlaskForm):
    # 讓使用者輸入 email 的欄位
    email = StringField('Email 請輸入信箱', validators=[DataRequired(), Email()])
    # 當使用者輸入完 email 後，要去數據庫確認該 email 是否存在
    submit = SubmitField('Send Email 寄送郵件')
    def validate_email(self, email):
        user_FormCheck = User.query.filter_by(email=email.data).first()
        # 若 email 不存在
        if not user_FormCheck:
            raise ValidationError('This email does not exist. 此電子郵件不存在。')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password 請輸入密碼', validators=[DataRequired(), Length(min=8, max=20)])
    comfirm = PasswordField('Repeat Password 請再次輸入密碼已確認', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password 重設密碼')

class PostTweetForm(FlaskForm):
    text = TextAreaField("Say something! 寫點東西吧!", validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Post! 貼文!')
