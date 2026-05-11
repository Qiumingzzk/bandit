"""
扫描任务路由：启动扫描、查询结果。
支持异步后台执行，避免阻塞。
"""
import threading
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import ScanTask, db
from app.scan_logic import run_scan_async

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/new', methods=['GET'])
@login_required
def new_scan_form():
    """新建扫描页面"""
    return render_template('new_scan.html')

@scan_bp.route('/start', methods=['POST'])
@login_required
def start_scan():
    """启动扫描，返回任务ID"""
    target = request.form.get('target') or request.json.get('target')
    if not target:
        return jsonify({'error': '目标不能为空'}), 400

    # 限制用户并发扫描数（可选）
    running_count = ScanTask.query.filter_by(user_id=current_user.id, status='running').count()
    max_concurrent = current_app.config.get('MAX_CONCURRENT_SCANS', 3)
    if running_count >= max_concurrent:
        return jsonify({'error': f'您已有 {running_count} 个扫描任务在运行，请稍后再试'}), 429

    task = ScanTask(
        user_id=current_user.id,
        target=target,
        status='pending'
    )
    db.session.add(task)
    db.session.commit()

    # 在后台线程中执行扫描
    thread = threading.Thread(target=run_scan_async, args=(task.id, target))
    thread.daemon = True
    thread.start()

    # 返回202 Accepted，前端可轮询
    return jsonify({'task_id': task.id, 'status': 'pending'}), 202

@scan_bp.route('/result/<int:task_id>', methods=['GET'])
@login_required
def get_result(task_id):
    """获取扫描结果（轮询接口）"""
    task = ScanTask.query.get(task_id)
    if not task:
        return jsonify({'error': '任务不存在'}), 404
    if task.user_id != current_user.id:
        return jsonify({'error': '无权访问'}), 403

    response = {
        'task_id': task.id,
        'status': task.status,
        'target': task.target,
        'created_at': task.created_at.isoformat(),
        'result': None,
        'error': task.error_msg
    }
    if task.status == 'completed':
        response['result'] = task.result
    return jsonify(response)