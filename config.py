#token
SECRET_KEY = "ajwijdilf"

# 数据库配置
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "573986"
DATABASE = "admin_db"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True


# 邮箱配置
MAIL_SERVER = "smtp.163.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "cwt15572060621@163.com"
MAIL_PASSWORD = "CRqgdADmVUBdJ3kg"
MAIL_DEFAULT_SENDER = "cwt15572060621@163.com"

