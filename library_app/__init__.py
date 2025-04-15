import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from enum import Enum

class MaxMinNumbers(Enum):
    TITLE_MAX = 64

app = Flask(__name__)

# todo: 秘密鍵の適切な設定、別の場所での保存
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
# todo: データベースをSQLiteからPostgreSQLに変更する
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# uri = os.environ.get('DATABASE_URL')  # 環境変数からデータベースのURLを取得
# if uri:  # Heroku などの環境変数から取得した場合
#     if uri.startswith('postgres://'):
#         uri = uri.replace('postgres://', 'postgresql://', 1)  # PostgreSQL の場合
#         app.config['SQLALCHEMY_DATABASE_URI'] = uri  # PostgreSQL のURLを設定
# else:  # SQLite の場合（ローカルの場合）
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hpXhNpM-ffN4jy4!CVEhn2MAo8T68bw_@localhost'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


def localize_callback(*args, **kwargs):
    return 'このページにアクセスするには、ログインが必要です。'


login_manager.localize_callback = localize_callback

# todo: DBの接続をPostgreSQLに変更する
from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


from library_app.main.views import main
from library_app.users.views import users
from library_app.books.views import books
from library_app.error_pages.handlers import error_pages

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(books)
app.register_blueprint(error_pages)
