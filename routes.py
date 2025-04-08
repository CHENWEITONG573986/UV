# -*- coding: utf-8 -*-
"""
路由定义

定义API路由，处理紫外线设备数据的接收和存储
"""

from flask import Blueprint, request, jsonify
from models import db, UVRecord

# 创建蓝图
api_bp = Blueprint('api', __name__)

@api_bp.route('/record', methods=['POST'])
def add_record():
    """
    添加紫外线检测记录
    
    接收设备传入的紫外线强度、温度、湿度和设备ID，并存储到数据库
    
    请求体格式:
    {
        "device_id": "设备ID",
        "uv_intensity": 紫外线强度,
        "temperature": 温度,
        "humidity": 湿度
    }
    
    返回:
        JSON响应，包含操作状态和消息
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 验证必要字段
        required_fields = ['device_id', 'uv_intensity', 'temperature', 'humidity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'缺少必要字段: {field}'
                }), 400
        
        # 验证数据类型
        try:
            device_id = str(data['device_id'])
            uv_intensity = float(data['uv_intensity'])
            temperature = float(data['temperature'])
            humidity = float(data['humidity'])
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': '数据类型错误，请确保紫外线强度、温度和湿度为数值类型'
            }), 400
        
        # 创建新记录
        new_record = UVRecord(
            device_id=device_id,
            uv_intensity=uv_intensity,
            temperature=temperature,
            humidity=humidity
        )
        
        # 保存到数据库
        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '数据记录成功',
            'data': new_record.to_dict()
        }), 201
        
    except Exception as e:
        # 回滚事务
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

@api_bp.route('/records', methods=['GET'])
def get_records():
    """
    获取紫外线检测记录列表
    
    可选查询参数:
    - device_id: 按设备ID筛选
    - limit: 限制返回记录数量，默认100条
    
    返回:
        JSON响应，包含记录列表
    """
    try:
        # 获取查询参数
        device_id = request.args.get('device_id')
        limit = request.args.get('limit', 100, type=int)
        
        # 构建查询
        query = UVRecord.query
        if device_id:
            query = query.filter_by(device_id=device_id)
        
        # 获取记录并按时间倒序排序
        records = query.order_by(UVRecord.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'count': len(records),
            'data': [record.to_dict() for record in records]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500

@api_bp.route('/records/<device_id>/latest', methods=['GET'])
def get_latest_record(device_id):
    """
    获取指定设备的最新记录
    
    参数:
        device_id: 设备ID
    
    返回:
        JSON响应，包含最新记录
    """
    try:
        # 查询指定设备的最新记录
        record = UVRecord.query.filter_by(device_id=device_id).order_by(UVRecord.created_at.desc()).first()
        
        if not record:
            return jsonify({
                'success': False,
                'message': f'未找到设备 {device_id} 的记录'
            }), 404
        
        return jsonify({
            'success': True,
            'data': record.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'服务器错误: {str(e)}'
        }), 500