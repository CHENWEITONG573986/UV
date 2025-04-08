# 紫外线设备检测仪器后端服务

这是一个基于Flask的后端服务程序，用于接收紫外线检测仪器传入的数据并存储到MySQL数据库中。

## 功能特点

- 接收并存储紫外线强度、温度、湿度和设备ID数据
- 提供RESTful API接口
- 数据存储到MySQL数据库
- 支持查询历史记录和最新记录

## 项目结构

```
.
├── .env                # 环境变量配置文件
├── app.py             # Flask应用入口
├── models.py          # 数据库模型定义
├── routes.py          # API路由定义
├── requirements.txt   # 项目依赖
└── README.md          # 项目说明文档
```

## 安装与配置

1. 安装依赖包

```bash
pip install -r requirements.txt
```

2. 配置数据库

编辑 `.env` 文件，设置数据库连接信息：

```
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=uv_device_db
```

3. 创建数据库

在MySQL中创建数据库：

```sql
CREATE DATABASE uv_device_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 运行服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 上运行。

## API接口说明

### 1. 添加紫外线检测记录

- **URL**: `/api/record`
- **方法**: POST
- **请求体**:

```json
{
    "device_id": "设备ID",
    "uv_intensity": 紫外线强度,
    "temperature": 温度,
    "humidity": 湿度
}
```

- **成功响应** (201):

```json
{
    "success": true,
    "message": "数据记录成功",
    "data": {
        "id": 1,
        "device_id": "设备ID",
        "uv_intensity": 紫外线强度,
        "temperature": 温度,
        "humidity": 湿度,
        "created_at": "2023-09-01 12:00:00"
    }
}
```

### 2. 获取紫外线检测记录列表

- **URL**: `/api/records`
- **方法**: GET
- **查询参数**:
  - `device_id`: (可选) 按设备ID筛选
  - `limit`: (可选) 限制返回记录数量，默认100条

- **成功响应** (200):

```json
{
    "success": true,
    "count": 1,
    "data": [
        {
            "id": 1,
            "device_id": "设备ID",
            "uv_intensity": 紫外线强度,
            "temperature": 温度,
            "humidity": 湿度,
            "created_at": "2023-09-01 12:00:00"
        }
    ]
}
```

### 3. 获取指定设备的最新记录

- **URL**: `/api/records/{device_id}/latest`
- **方法**: GET

- **成功响应** (200):

```json
{
    "success": true,
    "data": {
        "id": 1,
        "device_id": "设备ID",
        "uv_intensity": 紫外线强度,
        "temperature": 温度,
        "humidity": 湿度,
        "created_at": "2023-09-01 12:00:00"
    }
}
```

## 数据库结构

### uv_records 表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | Integer | 记录ID (主键) |
| device_id | String(50) | 设备ID |
| uv_intensity | Float | 紫外线强度 |
| temperature | Float | 温度(°C) |
| humidity | Float | 湿度(%) |
| created_at | DateTime | 记录创建时间 |