from flask import Flask, jsonify, render_template
from werkzeug.exceptions import HTTPException
from .config import Config
from .extensions import db, jwt, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from .auth.routes import auth_bp
    from .scan.routes import scan_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(scan_bp, url_prefix='/scan')

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"msg": e.description, "code": e.code}), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        app.logger.error(f"Unhandled exception: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    @app.route('/')
    def index():
        return render_template('index.html')

    return app