import jwt
import datetime
from flask import  jsonify, request
# 密钥，用于签名和验证 JWT
SECRET_KEY = "your_secret_key"

# 生成 JWT
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # 设置过期时间为 1 小时
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
# 验证token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print('Token 已过期')
    except jwt.InvalidTokenError:
        print('无效的 Token')
    return None

# 封装的 token 验证函数
def validate_token():
    # 从请求头中获取 token
    token = request.headers.get('x-token')

    # 检查 token 是否存在
    if not token:
        return jsonify({
            "code": -2,
            "message": "未提供 token",
            "data": None
        }), 401

    # 验证 token
    payload = verify_token(token)
    if not payload:
        return jsonify({
            "code": -2,
            "message": "无效的 token 或 token 已过期",
            "data": None
        }), 401

    return None, payload