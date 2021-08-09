from threading import Thread # 把單線程作業，變成多線程作業，以減少作業時間，提高效率 
from flask_mail import Message 
from flask import current_app, render_template

from app import mail, app

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

# sender 裡面的 config["MAIL_USERNAME"] 即為 config.py 裡面的 MAIL_USERNAME
def send_reset_password_mail(user, token):
    msg = Message("[Flask APP]Reset Your Password",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
        html=render_template("reset_password_mail.html", user=user, token=token))
    # mail.send(msg) # 將以上建立好的郵件發送
    # 因為要做多線程設計，把 mail.send(msg) 的功能挪到 send_async_mail()
    # 運用 Thread 做多線程功能
    Thread(target=send_async_mail, args=(app, msg)).start()
    # 每當前端做出寄送郵件的要求時，後端的 Thread 就會優先做出響應
