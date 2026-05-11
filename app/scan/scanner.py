import subprocess
import json
import os


def run_bandit_scan(target_path: str):
    if not os.path.exists(target_path):
        return {"error": f"Path does not exist: {target_path}"}

    abs_path = os.path.abspath(target_path)

    # 使用配置文件 + profile 方式加载插件
    cmd = [
        'bandit', abs_path,
        '-c', '/app/.bandit',  # 配置文件路径（容器内）
        '-p', 'custom',  # 使用配置文件中的 custom profile
        '-f', 'json',
        '--quiet'
    ]

    # 设置 PYTHONPATH 以确保 Bandit 能找到 custom_rules 包
    env = os.environ.copy()
    env['PYTHONPATH'] = '/app'

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        if result.stdout:
            return json.loads(result.stdout)
        else:
            return {"error": "No output", "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"error": "Scan timeout (120s)"}
    except Exception as e:
        return {"error": str(e)}