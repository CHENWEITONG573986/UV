
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from sqlalchemy.sql.functions import current_user

from exts import mail,db
from flask_mail import Message
import string
import random
from models import EmailCaptchaModel,UserModel,PermissionsModel
from .froms import RegisterForm,LoginForm,PermissionsForm
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from datetime import datetime, timedelta
from  .token import generate_token,verify_token,validate_token
import json
bp = Blueprint("admin", __name__, url_prefix='/')


# 定义权限 ID 到权限名称的映射
PERMISSION_MAPPING = {
    1: '控制台',
    2: '权限管理',
    3: 'DIDI陪诊',
    4: '账号管理',
    5: '菜单管理',
    6: '陪护管理',
    7: '订单管理'
}

@bp.route('/auth/admin', methods=['GET'])
def admin():
    error_response, payload = validate_token()
    if error_response:
        return error_response
    # 若 token 验证成功，可以在这里添加具体的业务逻辑，例如查询数据库获取权限管理列表等
    users = UserModel.query.all()
    total = len(users)
    # 将查询结果转换为列表，每个元素是一个字典
    data = []
    for user in users:
        u = {
            'id': user.id,  # 假设表中有 id 字段
            'name': user.username,  # 假设表中有 name 字段
            'email': user.email,
            'permissions': user.permissions.name,
            'permissions_id': user.permissions_id,
            'join_time': user.join_time.strftime('%Y-%m-%d'),
            'active': 1
        }
        data.append(u)
    return jsonify({
        "code": 200,
        "message": "读取成功",
        "data": {
            "list": data,
            "total": total
        }
    })

@bp.route('/user/getmenu', methods=['GET'])
def usermenu():
    error_response, payload = validate_token()
    if error_response:
        return error_response
    # 若 token 验证成功，可以在这里添加具体的业务逻辑，例如查询数据库获取权限管理列表等
    Tree = [
    {
        "id": 1,
        "label": "控制台",
    },
    {
        "id": 2,
        "label": "权限管理",
        "children": [
            {
                "id": 4,
                "label": "账号管理"
            },
            {
                "id": 5,
                "label": "菜单管理"
            }
        ]
    },
    {
        "id": 3,
        "label": "DIDI陪诊",
        "children": [
            {
                "id": 6,
                "label": "陪护管理"
            },
            {
                "id": 7,
                "label": "订单管理"
            }
        ]
    }
]

    return jsonify({
        "code": 200,
        "message": "读取成功",
        "data": Tree,
    })

@bp.route('/user/setmenu', methods=['POST'])
def setmenu():
    error_response, payload = validate_token()
    if error_response:
        return error_response
    # 若 token 验证成功，可以在这里添加具体的业务逻辑，例如查询数据库获取权限管理列表等

    data = request.get_json()
    form = PermissionsForm(data=data)
    print(form.name.data)
    print(form.permissions.data)
    if form.validate():
        name = form.name.data
        permissions = form.permissions.data
        pm = PermissionsModel(name=name, permissions=permissions)
        db.session.add(pm)
        db.session.commit()
        return jsonify({"code": 200, "message": "添加成功", "data": None})
    else:
        print("errors")
        return jsonify({"code": 500, "message": "添加失败", "data": None})

def get_permissions_name(permissions_data):
    """
    根据权限数据列表生成权限名称字符串
    :param permissions_data: 权限数据列表
    :return: 权限名称字符串
    """
    names = [PERMISSION_MAPPING.get(perm_id) for perm_id in permissions_data if perm_id in PERMISSION_MAPPING]
    return "，".join(names)

@bp.route('/menu/list', methods=['GET'])
def menulist():
    error_response, payload = validate_token()
    if error_response:
        return error_response
    # 若 token 验证成功，可以在这里添加具体的业务逻辑，例如查询数据库获取权限管理列表等
    # 查询 PermissionsModel 表的所有数据
    # 查询 PermissionsModel 表的所有数据
    permissions = PermissionsModel.query.all()
    total = len(permissions)

    # 将查询结果转换为列表，每个元素是一个字典
    permission_list = []
    for permission in permissions:
        try:
            # 解析 JSON 格式的权限数据
            permissions_data = json.loads(permission.permissions)
        except (ValueError, TypeError):
            # 若解析失败，设置为空列表
            permissions_data = []

        # 获取权限名称字符串
        permissionsName = get_permissions_name(permissions_data)

        permission_dict = {
            'id': permission.id,  # 假设表中有 id 字段
            'name': permission.name,  # 假设表中有 name 字段
            'permissions': permissions_data,
            'permissionsName': permissionsName
        }
        permission_list.append(permission_dict)

    return jsonify({
        "code": 200,
        "message": "设置成功",
        "data": {
            "list": permission_list,
            "total": total
        }
    })

@bp.route('/menu/selectlist', methods=['GET'])
def selectlist():
    error_response, payload = validate_token()
    if error_response:
        return error_response
    # 若 token 验证成功，可以在这里添加具体的业务逻辑，例如查询数据库获取权限管理列表等
    users = UserModel.query.all()
    total = len(users)
    # 将查询结果转换为列表，每个元素是一个字典
    data = []
    for user in users:
        u = {
            'id': user.id,  # 假设表中有 id 字段
            'name': user.username,  # 假设表中有 name 字段
            'email': user.email,
            'permissions': user.permissions.name,
            'permissions_id': user.permissions_id,
            'join_time': user.join_time
        }
        data.append(u)
    return jsonify({
        "code": 200,
        "message": "设置成功",
        "data": {
            "list": data,
            "total": total
        }
    })