# 导入所有蓝图
from .test_user_routes import test_user_bp
from .tb_item_routes import tb_item_bp
from .auth_routes import auth_bp

# 将所有蓝图添加到列表中
all_blueprints = [
    (test_user_bp, ""),
    (tb_item_bp, ""),
    (auth_bp, "/api")
]

def register_blueprints(app):
    for blueprint, url_prefix in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)

