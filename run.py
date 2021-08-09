#【Flask 教程】11 - 判斷用戶名和密碼是否存在於數據庫中
# https://youtu.be/L_pc1BDNYHQ

# 製作當註冊成功後，產生自動跳轉到 index 頁面的功能。
# from flask import redirect, url_for
# 並且在 route 中添加新邏輯
# return redirect(url_for('index'))

from app import app

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 3000)