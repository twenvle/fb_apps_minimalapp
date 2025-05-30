from datetime import datetime

from apps.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# db.Modelに継承することで，これはデータベースのテーブルと繋がるクラスであるとFlaskに伝えている
class User(db.Model, UserMixin):  # userクラスは，データベースとpythonの橋渡し役
    __tablename__ = "users"  # データベースのテーブル名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, index=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # backrefを利用しrelation情報を設定する
    user_images = db.relationship("UserImage", backref="user")

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    # print(user.password) -> AttributeError: 読み取り不可
    # ・パスワードは見せない
    # ・間違ってもコードから表示できないように
    # セキュリティ対策

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 生のパスワードを受け取ったらgenerate_password_hash()によってハッシュ化して保存する

    # パスワードチェックをする
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # メールアドレス重複チェックをする
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


# ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
