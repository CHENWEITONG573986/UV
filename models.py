from exts import db
from datetime import datetime

class PermissionsModel(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    permissions = db.Column(db.String(100), nullable=False)

class UVModel(db.Model):
    __tablename__ = "uv"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    esp_id = db.Column(db.Integer, nullable=False)
    uv_value = db.Column(db.Float, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False , unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    permissions_id = db.Column(db.Integer,db.ForeignKey('permissions.id'))
    permissions = db.relationship(PermissionsModel, backref='user')

    UV_id = db.Column(db.Integer, db.ForeignKey('uv.id'))
    UV = db.relationship(UVModel, backref='user')

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    email = db.Column(db.String(100), primary_key=True, nullable=False , unique=True)
    captcha = db.Column(db.String(100), nullable=False)

