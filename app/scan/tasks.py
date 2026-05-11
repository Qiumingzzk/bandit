import threading
from datetime import datetime
from app.models import ScanTask, db
from .scanner import run_bandit_scan

def start_async_scan(task_id: int, target_path: str):
    def _run():
        from app import create_app
        app = create_app()
        with app.app_context():
            task = ScanTask.query.get(task_id)
            if not task:
                app.logger.error(f"Task {task_id} not found")
                return
            try:
                task.status = 'running'
                db.session.commit()
                app.logger.info(f"Starting scan for task {task_id}, path: {target_path}")
                result = run_bandit_scan(target_path)
                task.status = 'completed'
                task.result = result
                task.completed_at = datetime.utcnow()
                db.session.commit()
                app.logger.info(f"Scan completed for task {task_id}")
            except Exception as e:
                app.logger.error(f"Scan failed for task {task_id}: {str(e)}", exc_info=True)
                task.status = 'failed'
                task.result = {"error": str(e)}
                db.session.commit()
    threading.Thread(target=_run, daemon=True).start()