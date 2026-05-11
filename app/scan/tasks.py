from ..extensions import celery, db
from .scanner import run_bandit_scan
from ..models import ScanTask
from datetime import datetime

@celery.task(bind=True)
def async_scan_task(self, task_id: int, target_path: str):
    """
    异步执行 Bandit 扫描，更新任务状态和结果
    """
    try:
        # 更新状态为 running
        task = ScanTask.query.get(task_id)
        if not task:
            return {"error": "任务不存在"}
        task.status = 'running'
        db.session.commit()

        # 执行扫描
        result = run_bandit_scan(target_path)

        # 更新完成状态
        task.status = 'completed'
        task.result = result
        task.completed_at = datetime.utcnow()
        db.session.commit()
        return result
    except Exception as e:
        task = ScanTask.query.get(task_id)
        if task:
            task.status = 'failed'
            task.result = {"error": str(e)}
            db.session.commit()
        raise e