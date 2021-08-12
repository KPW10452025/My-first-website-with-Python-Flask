from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username 請輸入使用者名稱', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email 請輸入信箱', validators=[DataRequired(), Email()])
    password = PasswordField('Password 請輸入密碼', validators=[DataRequired(), Length(min=8, max=20)])
    comfirm = PasswordField('Repeat Password 請再次輸入密碼已確認', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('OK and Register 確認並提交')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already registered. 此用戶名已被註冊。')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is already registered. 此信箱已被註冊。')

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
