"""
主页路由。
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """用户仪表盘，展示最近的扫描任务"""
    from app.models import ScanTask
    recent_scans = ScanTask.query.filter_by(user_id=current_user.id).order_by(ScanTask.created_at.desc()).limit(10).all()
    return render_template('dashboard.html', scans=recent_scans)