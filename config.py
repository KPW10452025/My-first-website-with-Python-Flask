# 此文檔用來設定 config

import os

from dotenv import load_dotenv # 利用 dotenv 載入環境變數
load_dotenv() # dotenv 基本語法 # take environment variables from .env

class Config(object): # 默認語法 
    
    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 減少運算
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.db' # 選擇要使用的 database 並設定連接此 database 的位置

    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # RECAPTCHA KEY
    # 需要去 google 申請
    # https://www.google.com/recaptcha/admin/site/454519195/settings
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    # flask-mail by gmail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("GMAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")
