from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from sqlalchemy import event
from sqlalchemy.engine import Engine

app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
jwt = JWTManager(app)

def configure_logging(app):
    if not app.debug:
        # 确保日志目录存在
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )

        # 设置控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)  # 确保控制台处理器的日志级别
        app.logger.addHandler(console_handler)

        # 设置时间滚动文件日志处理器
        file_handler = TimedRotatingFileHandler(
            'logs/app.log', when='midnight', interval=1, backupCount=30
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.DEBUG)  # 确保应用的日志级别
        app.logger.info('App startup')

configure_logging(app)

# 添加蓝图（导入并注册所有路由）
from app.routes.test_user_routes import test_user_bp
from app.routes.tb_item_routes import tb_item_bp
from app.routes.auth_routes import auth_bp

app.register_blueprint(test_user_bp)
app.register_blueprint(tb_item_bp)
app.register_blueprint(auth_bp, url_prefix='/api')

# 记录 Flask 请求
@app.before_request
def log_request_info():
    app.logger.debug(f'Request: {request.method} {request.url}')
    app.logger.info(f'Headers: {request.headers}')
    app.logger.info(f'Body: {request.get_data()}')

@app.after_request
def log_response_info(response):
    app.logger.info(f'Response status: {response.status}')
    app.logger.info(f'Response headers: {response.headers}')
    return response

# 记录数据库操作
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    app.logger.info(f"Start Query: {statement}")
    app.logger.debug(f"Parameters: {parameters}")

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    app.logger.info("Query Complete")

@event.listens_for(Engine, "handle_error")
def handle_error(context):
    app.logger.error("Query Failed")


# 统一错误处理
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'Unhandled Exception: {str(e)}')
    response = {
        'message': 'An unexpected error occurred.',
        'details': str(e)
    }
    return jsonify(response), 500
