from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from exts import mail,db
from flask_mail import Message
import string
import random
from models import EmailCaptchaModel,UserModel
from .froms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from datetime import datetime, timedelta
from  .token import generate_token,verify_token
bp = Blueprint("auth", __name__, url_prefix='/')


@bp.route('/get/code', methods=['POST'])
def get_email_captcha():
    # 从请求参数中获取邮箱地址
    data = request.get_json()
    if not data or 'tel' not in data:
        return jsonify({"code": -1, "message": "请提供邮箱地址"}), 400
    # 从请求参数中获取邮箱地址
    #email = request.args.get("email")
    email = data['tel']
    print(email)
    # 生成验证码
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    print(captcha)
    # 发送验证码邮件
    message = Message("注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
    mail.send(message)
    # 查询数据库中是否已经存在该邮箱对应的记录
    existing_record = EmailCaptchaModel.query.filter_by(email=email).first()
    if existing_record:
        # 如果记录存在，更新验证码
        existing_record.captcha = captcha
    else:
        # 如果记录不存在，创建新的记录
        email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)

    try:
        # 提交数据库会话
        db.session.commit()
        return jsonify({"code": 200, "message": "验证码发送成功", "data": None})
    except Exception as e:
        # 出现异常，回滚数据库会话
        db.session.rollback()
        return jsonify({"code": 500, "message": f"数据库操作出错: {str(e)}", "data": None})

@bp.route('user/auth', methods=['POST'])
def register():
    data = request.get_json()
    form = RegisterForm(data = data)
    if form.validate():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = UserModel(email=email, username=username, password=generate_password_hash(password),permissions_id = 1)
        db.session.add(user)
        db.session.commit()
        return jsonify({"code": 200, "message": "注册成功", "data": None})
    else:
        print("errors")
        return jsonify({"code": 500, "message": "注册失败", "data": None})

@bp.route('/login', methods=['POST'])
def login():
    print("login")
    data = request.get_json()
    form = LoginForm(data=data)
    print(form.username.data)
    print(form.password.data)
    if form.validate():
        print("valid")
        username = form.username.data
        password = form.password.data
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return jsonify({"code": 500, "message": "账号错误", "data": None})
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            user_info = {
                'username': username,
                'email': user.email,
                'id': user.id,
            }
            token = generate_token(user.id)
            print("登录成功")
            return jsonify({
                "code": 200,
                "message": "登录成功",
                "data":{
                    'token': token,
                    'userInfo': user_info
            } })
        else:
            return jsonify({"code": 500, "message": "密码错误", "data": None})
    else:
        print("errors")
        return jsonify({"code": 500, "message": "登录失败", "data": None})