from flask import Flask, request, jsonify, session, make_response
from exts import db, mail
from flask_migrate import Migrate
import config
from blueprints.auth import bp as auth_bp
from blueprints.admin import bp as admin_bp
from blueprints.value import bp as value_bp
from flask_cors import CORS  # 导入 CORS 扩展

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/')
app.register_blueprint(value_bp, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True)