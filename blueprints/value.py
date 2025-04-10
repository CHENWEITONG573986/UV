from flask import request, jsonify, Blueprint
from .token import validate_token
from datetime import datetime, timedelta
from models import UVModel
from exts import db
import json

bp = Blueprint("value", __name__, url_prefix='/')

# 定义电压区间和对应等级的字典
voltage_level_mapping = {
    50: 0,
    227: 1,
    318: 2,
    408: 3,
    503: 4,
    606: 5,
    696: 6,
    795: 7,
    881: 8,
    976: 9,
    1079: 10,
    1170: 11
}

# 定义一个函数来根据电压获取等级
def get_voltage_level(voltage):
    for threshold, level in sorted(voltage_level_mapping.items()):
        if voltage < threshold:
            return level
    # 如果电压大于等于最大阈值，这里可以根据实际情况处理，例如返回一个默认值
    return 12

@bp.route('/upload', methods=['POST'])
def upload_data():
    try:
        data = request.get_json()
        id = data.get('id')
        voltage = data.get('voltage')
        level = get_voltage_level(voltage)
        UV = UVModel(esp_id=id, uv_value=voltage, level=level)
        db.session.add(UV)
        db.session.commit()
        print(f"id: {id},  Voltage: {voltage} mV")
        # 在这里可以将数据存储到数据库或进行其他处理
        return jsonify({"status": "success", "message": "Data received successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@bp.route('/UVvalue', methods=['POST'])
def getUVvalue():
    error_response, payload = validate_token()
    if error_response:
        return error_response
    # 获取前端传递的参数，判断是否请求近一周数据
    data = request.get_json()
    selected_date = data.get('selected_date', 'today')

    uvData = []
    riskData = []
    riskLevels = ["无风险", "低风险", "中风险", "高风险", "极高风险"]

    # 获取 UVModel 表中的数据
    if selected_date == 'yesterday':
        start_date = datetime.now() - timedelta(days=1)
        end_date = start_date + timedelta(days=1)
        records = UVModel.query.filter(UVModel.time >= start_date, UVModel.time < end_date).all()
    elif selected_date == 'the_day_before_yesterday':
        start_date = datetime.now() - timedelta(days=2)
        end_date = start_date + timedelta(days=1)
        records = UVModel.query.filter(UVModel.time >= start_date, UVModel.time < end_date).all()
    elif selected_date == 'past_week':
        start_date = datetime.now() - timedelta(days=6)
        records = UVModel.query.filter(UVModel.time >= start_date).all()
    else:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        records = UVModel.query.filter(UVModel.time >= start_date, UVModel.time < end_date).all()

    for record in records:
        # 修改时间格式为精确到分钟
        time_str = record.time.strftime("%m-%d %H:%M")
        intensity = record.uv_value
        uvData.append([time_str, intensity])

    # 重新计算风险等级（根据过滤后的数据）
    total_time = len(uvData)
    risk_counts = [0, 0, 0, 0, 0]
    for record in records:
        level = record.level
        if level in [0, 1, 2]:
            risk_counts[0] += 1
        elif level in [3, 4, 5]:
            risk_counts[1] += 1
        elif level in [6, 7, 8]:
            risk_counts[2] += 1
        elif level in [9, 10, 11]:
            risk_counts[3] += 1
        elif level == 12:
            risk_counts[4] += 1

    riskData = [
        [riskLevels[0], risk_counts[0]],
        [riskLevels[1], risk_counts[1]],
        [riskLevels[2], risk_counts[2]],
        [riskLevels[3], risk_counts[3]],
        [riskLevels[4], risk_counts[4]]
    ]

    response_data = {
        "code": 200,
        "data": {
            "uvIntensityData": uvData,
            "riskLevelData": riskData
        },
        "message": "数据获取成功"
    }

    return jsonify(response_data)

@bp.route('/getCurrentUV', methods=['GET'])
def get_current_uv():
    error_response, payload = validate_token()
    if error_response:
        return error_response
    # 获取最新的紫外线强度数据
    latest_record = UVModel.query.order_by(UVModel.time.desc()).first()
    if latest_record:
        uv_value = latest_record.uv_value
    else:
        uv_value = 0

    response_data = {
        "code": 200,
        "data": {
            "uvValue": uv_value
        },
        "message": "当前紫外线强度获取成功"
    }
    return jsonify(response_data)