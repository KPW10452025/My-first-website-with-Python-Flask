from flask import render_template, flash, redirect, url_for, request
from app import app, bcrypt, db
from app.forms import RegisterForm
from app.forms import LoginForm
from app.forms import PasswordResetRequestForm
from app.forms import ResetPasswordForm
from app.forms import PostTweetForm
from app.models import User
from app.models import Post
from app.email import send_reset_password_mail
from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user

@app.route("/", methods=["Get", "Post"])
@login_required
def index():
    form = PostTweetForm()
    if form.validate_on_submit(): 
        body = form.text.data
        post = Post(body=body)
        current_user.posts.append(post)
        db.session.commit()
        flash("You have post a new tweet!", category='info')
        flash("您發布了一條新推文!", category='info')
    n_followers = len(current_user.followers)
    n_followed = len(current_user.followed)
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 2, False)
    # 在 route index 中新增 posts 並從數據庫中提取 Post 資料
    # 在 return 中回傳 posts = posts
    return render_template("index.html", title = "Home", form = form, posts = posts, 
    n_followers = n_followers, n_followed = n_followed)

@app.route("/user_page/<username>")
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        page = request.args.get("page", 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 2, False)
        return render_template("user_page.html", user=user, posts=posts)
    else:
        return '404'

@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user:
        current_user.follow(user)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 2, False)
        return render_template("user_page.html", user=user, posts=posts)
    else:
        return '404'

@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user:
        current_user.unfollow(user)
        db.session.commit()
        page = request.args.get("page", 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 2, False)
        return render_template("user_page.html", user=user, posts=posts)
    else:
        return '404'

@app.route("/register", methods=["Get", "Post"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        print(username, email, password)
        user = User(username = username, email = email, password = password)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, the registration is successful.", category="success")
        return redirect(url_for('login'))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remenber = form.remember.data
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remenber)
            flash("Log In Suceesfully!", category="info")
            flash("登入成功!", category="info")
            if request.args.get("next"):
                next_page = request.args.get("next")
                return redirect(next_page) 
            return redirect(url_for("index"))
        flash("The user does not exist or the password is incorrect.", category="danger")
        flash("用戶不存在或是密碼不正確。", category="danger")
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out!", category="warning")
    flash("你已經登出!", category="warning")
    return redirect(url_for("login"))

@app.route("/send_password_reset_request", methods=["GET", "POST"])
def send_password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email_check = form.email.data
        user = User.query.filter_by(email=email_check).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token)
        flash("Password reset request mail is sent, please check your mail.", category="info")
        flash("密碼重置請求郵件已發送，請檢查您的郵件。", category="info")
    return render_template("send_password_reset_request.html", title = "Request", form = form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if form.validate_on_submit():
        user = User.check_reset_password_token(token) 
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash("Password has been updated.", category="success")
            flash("密碼已更新。", category="success")
            return redirect(url_for("login"))
        else:
            flash("The user is not exists.", category="danger")
            flash("用戶不存在。", category="danger")
            return redirect(url_for("login"))
    return render_template("reset_password.html", title = "Reset", form = form)
        