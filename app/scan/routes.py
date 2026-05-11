from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import ScanTask, db
from .tasks import async_scan_task

scan_bp = Blueprint('scan', __name__)


@scan_bp.route('/start', methods=['POST'])
@jwt_required()
def start_scan():
    """发起扫描任务（异步）"""
    data = request.get_json()
    if not data or 'name' not in data or 'path' not in data:
        return jsonify({"msg": "缺少任务名称或扫描路径"}), 400

    user_id = int(get_jwt_identity())
    task = ScanTask(
        user_id=user_id,
        task_name=data['name'],
        target_path=data['path'],
        status='pending'
    )
    db.session.add(task)
    db.session.commit()

    # 异步执行
    async_scan_task.delay(task.id, data['path'])

    return jsonify({"task_id": task.id, "status": "pending"}), 202


@scan_bp.route('/result/<int:task_id>', methods=['GET'])
@jwt_required()
def get_result(task_id):
    """查询扫描结果"""
    # 可选：验证当前用户是否有权查看该任务
    task = ScanTask.query.get_or_404(task_id)
    return jsonify({
        "status": task.status,
        "result": task.result,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None
    }), 200


@scan_bp.route('/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    """获取当前用户的所有扫描任务"""
    user_id = int(get_jwt_identity())
    tasks = ScanTask.query.filter_by(user_id=user_id).order_by(ScanTask.created_at.desc()).all()
    return jsonify([{
        "id": t.id,
        "task_name": t.task_name,
        "target_path": t.target_path,
        "status": t.status,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "completed_at": t.completed_at.isoformat() if t.completed_at else None
    } for t in tasks]), 200