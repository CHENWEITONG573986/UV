# -*- coding: utf-8 -*-
"""
数据库模型定义

定义与紫外线设备检测相关的数据库模型
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建SQLAlchemy实例
db = SQLAlchemy()

class UVRecord(db.Model):
    """
    紫外线检测记录模型
    
    存储设备ID、紫外线强度、温度、湿度以及记录时间
    """
    __tablename__ = 'uv_records'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='记录ID')
    device_id = db.Column(db.String(50), nullable=False, index=True, comment='设备ID')
    uv_intensity = db.Column(db.Float, nullable=False, comment='紫外线强度')
    temperature = db.Column(db.Float, nullable=False, comment='温度(°C)')
    humidity = db.Column(db.Float, nullable=False, comment='湿度(%)')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    
    def __repr__(self):
        return f"<UVRecord(id={self.id}, device_id='{self.device_id}', uv_intensity={self.uv_intensity})>"
    
    def to_dict(self):
        """
        将模型转换为字典
        
        返回:
            包含模型数据的字典
        """
        return {
            'id': self.id,
            'device_id': self.device_id,
            'uv_intensity': self.uv_intensity,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }