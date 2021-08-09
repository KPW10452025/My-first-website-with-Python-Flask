from flask import render_template, flash, redirect, url_for, request
from app import app, bcrypt, db
from app.forms import RegisterForm # 製作 Register 頁面時會用到的，從 forms.py 載入 class RegisterForm
from app.forms import LoginForm # 製作 Login 頁面時會用到的，從 forms.py 載入 class LoginForm
from app.forms import PasswordResetRequestForm
from app.forms import ResetPasswordForm
from app.forms import PostTweetForm # 加到 @app.route("/") 裡面，添加主頁新功能
from app.models import User # 當前端輸入資料時，需要將資料存到資料庫中
from app.models import Post
from app.email import send_reset_password_mail
from flask_login import login_user # 用戶通過認證後，使用 login_user 函數將他們登錄
from flask_login import login_required # login_required 製作需登入才有訪問權的頁面 
from flask_login import current_user # 使用 if current_user.is_authenticated: 來判斷用戶是否已登入
from flask_login import logout_user # 製作登出頁面


@app.route("/", methods=["Get", "Post"]) # 網站「首頁」
@login_required
def index():
    form = PostTweetForm()
    # 如果表格有寫入資料的話
    if form.validate_on_submit(): 
        body = form.text.data # 將 form 的 text 裡的數據變成 body
        post = Post(body=body) # 將 body 放入 table Post 
        current_user.posts.append(post) # 將 post 和當前使用者做連結
        db.session.commit()
        flash("You have post a new tweet!", category='info')
        flash("您發布了一條新推文!", category='info')
    return render_template("index.html", title = "Home", form = form)

@app.route("/register", methods=["Get", "Post"])
def register():
    if current_user.is_authenticated:
        # 如果用戶屬於登入狀態，讓用戶自動跳轉到 index
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        # password = form.password.data # 未加密
        password = bcrypt.generate_password_hash(form.password.data) #已加密，說明在下面：flask_bcrypt，或是看文檔 how_to_use_bcrypt.py
        print(username, email, password) # 測試用：當前端註冊後按下註冊鍵，成功的話，註冊資訊會顯示在 terminal 上面
        user = User(username = username, email = email, password = password) # 把前端輸入的資料放到 models.py 的 class User 裡
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, the registration is successful.", category="success")
        # flash 的底版顏色會由 bootstrap 語法決定
        # https://getbootstrap.com/docs/3.3/components/
        # default  白色
        # primary  藍色
        # success  綠色
        # info     天藍色
        # warning  橘色
        # danger   紅色
        return redirect(url_for('login'))
        # 註冊完自動跳轉到登入畫面
    return render_template("register.html", title = "Register", form = form)

# validate_on_submit() 功能為當前端已提交數據時，設定要如何處理數據

# flask_bcrypt 加密功能解說：假設使用者資訊：
# name = test0001
# email = test0001@gmail.com
# password = 12341234

# 未使用 bcrypt.generate_password_hash() 前
# password = form.password.data
# 之後使用 print(username, email, password) ternimal 會顯示完整的 password
# test0001 test0001@gmail.com 12341234

# 而使用 bcrypt.generate_password_hash() 後
# password = bcrypt.generate_password_hash(form.password.data)
# 之後使用 print(username, email, password) ternimal 會顯示加密的 password
# test0001 test0001@gmail.com b'$2b$12$ZjnzjfCODHcbNEt5oH3xdeBMFBGhknMULpCvKZSQwCvBwVmCLlOyq'

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # 如果用戶屬於登入狀態，讓用戶自動跳轉到 index
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remenber = form.remember.data
        # Use Bcrypt to check if password is match
        # go to batabase to find the username
        user = User.query.filter_by(username = username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # if true, it means the user is exist and the password is matched
            login_user(user, remember=remenber)
            flash("Log In Suceesfully!", category="info")
            flash("登入成功!", category="info")
            if request.args.get("next"):
                next_page = request.args.get("next")
                return redirect(next_page) 
                # 雖然是登入介面，但網址卻不是 login
                # 而是 http://localhost:3000/login?next=%2F
                # 用戶目前的狀態是一個名為 %2F 的 next 狀態
                # 而以上功能為讓用戶登入完後，就能直接跳轉回到剛才的頁面，也就是需登入才能訪問的頁面
            return redirect(url_for("index")) # 如果用戶是在 login 頁面做登入，則會跳轉到 index
        flash("The user does not exist or the password is incorrect.", category="danger")
        flash("用戶不存在或是密碼不正確。", category="danger")
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
@login_required # 這句語法的目的為：使用者只能在登入狀態時才能都出
# 如果沒有 @login_required 使用者即使沒有登入，直接輸入 url/logout 也會出現登出 flash 等怪現象
def logout():
    logout_user()
    flash("You have logged out!", category="warning")
    flash("你已經登出!", category="warning")
    return redirect(url_for("login"))

@app.route("/send_password_reset_request", methods=["GET", "POST"])
def send_password_reset_request():
    if current_user.is_authenticated:
        # 如果用戶屬於登入狀態，讓用戶自動跳轉到 index
        return redirect(url_for("index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email_check = form.email.data
        user = User.query.filter_by(email=email_check).first()
        # 因為在 form.py 裡的 PasswordResetRequestForm 裡的 def validate_email 已先判斷 user_FormCheck 的 email 是否存在
        # 所以能傳過來的 email 都是存在的，所以這邊不歐用再確認一次上方的 user
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token) # 這個函數 send_reset_password_mail() 寫在 email.py 裡面
        flash("Password reset request mail is sent, please check your mail.", category="info")
        flash("密碼重置請求郵件已發送，請檢查您的郵件。", category="info")
    return render_template("send_password_reset_request.html", title = "Request", form = form)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        # 如果用戶屬於登入狀態，讓用戶自動跳轉到 index
        return redirect(url_for("index"))
    if form.validate_on_submit():
        # 如果用戶做了填表的動作
        user = User.check_reset_password_token(token) 
        # check_reset_password_token(token) 函式會解密 token 判斷用戶是否存在，如果存在則會回傳 token 相對應的 user
        if user:
            # 如果 user 存在則運用 form.password.data 讀取 form 資料，並使用 bcrypt.generate_password_hash() 進行加密
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash("Password has been updated.", category="success")
            flash("密碼已更新。", category="success")
            # 當確定更新完密碼後，讓用戶傳送到登入介面
            return redirect(url_for("login"))
        else:
            # 如果 user 不存在，就 flash 一個 message
            flash("The user is not exists.", category="danger")
            flash("用戶不存在。", category="danger")
            # 並且將用戶回傳到 login
            return redirect(url_for("login"))
    return render_template("reset_password.html", title = "Reset", form = form)
        