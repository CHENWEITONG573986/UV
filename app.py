# -*- coding: utf-8 -*-
"""
紫外线设备检测仪器后端服务程序

这个Flask应用提供API接口，接收紫外线检测仪器传入的数据并存储到MySQL数据库中。
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from models import db
from routes import api_bp

# 加载环境变量
load_dotenv()

def create_app():
    """
    创建并配置Flask应用
    
    返回:
        Flask应用实例
    """
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 启用CORS跨域支持
    CORS(app)
    
    # 配置数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

# 创建应用实例
app = create_app()

# 创建数据库表
# 在Flask 2.0+中，before_first_request已被移除，改用with app.app_context()方式
with app.app_context():
    db.create_all()
    print("数据库表已创建")

if __name__ == '__main__':
    # 运行应用
    app.run(host='0.0.0.0', port=5000)