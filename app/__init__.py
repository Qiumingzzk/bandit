from flask import Flask, render_template, jsonify
from .config import Config
from .extensions import db, jwt, celery, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    celery.conf.update(app.config)

    # 注册蓝图
    from .auth.routes import auth_bp
    from .scan.routes import scan_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(scan_bp, url_prefix='/scan')

    # 全局错误处理：将 HTTP 异常也返回 JSON，避免 HTML 页面
    from werkzeug.exceptions import HTTPException
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = jsonify({"msg": e.description, "code": e.code})
        response.status_code = e.code
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        # 生产环境不应打印 traceback，开发时方便调试
        app.logger.error(f"Unhandled exception: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    @app.route('/')
    def index():
        return render_template('index.html')

    return app