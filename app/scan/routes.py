from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import ScanTask, db
from .tasks import start_async_scan

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/start', methods=['POST'])
@jwt_required()
def start_scan():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or 'target_path' not in data:
        return jsonify({"msg": "Missing target_path"}), 400
    task = ScanTask(
        user_id=int(user_id),
        task_name=data.get('task_name', f"Scan_{data['target_path']}"),
        target_path=data['target_path'],
        status='pending'
    )
    db.session.add(task)
    db.session.commit()
    start_async_scan(task.id, data['target_path'])
    return jsonify({"task_id": task.id, "status": "pending"}), 202

@scan_bp.route('/result/<int:task_id>', methods=['GET'])
@jwt_required()
def get_result(task_id):
    user_id = get_jwt_identity()
    task = ScanTask.query.filter_by(id=task_id, user_id=int(user_id)).first()
    if not task:
        return jsonify({"msg": "Task not found"}), 404
    return jsonify({
        "task_id": task.id,
        "task_name": task.task_name,
        "status": task.status,
        "target_path": task.target_path,
        "result": task.result,
        "created_at": task.created_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None
    })