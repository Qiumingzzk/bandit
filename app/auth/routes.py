from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import User, db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"msg": "缺少用户名或密码"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "用户已存在"}), 400

    # 使用默认的 pbkdf2:sha256 哈希方法，无需额外安装 bcrypt
    hashed = generate_password_hash(data['password'])
    user = User(username=data['username'], password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "注册成功"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录，返回 JWT token"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"msg": "缺少用户名或密码"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200
    return jsonify({"msg": "用户名或密码错误"}), 401


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """获取当前用户信息（示例）"""
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"msg": "用户不存在"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }), 200