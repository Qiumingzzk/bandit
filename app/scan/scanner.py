import subprocess
import json
import os


def run_bandit_scan(target_path: str):
    """
    执行 Bandit 扫描，加载自定义插件，返回 JSON 结果
    """
    # 确保路径存在
    if not os.path.exists(target_path):
        return {"error": f"路径不存在: {target_path}"}

    # 构建命令，加载自定义插件
    cmd = [
        'bandit', '-r', target_path,
        '-p', 'custom_rules.detect_insecure_deserialization',
        '-f', 'json', '--quiet'
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.stdout:
            return json.loads(result.stdout)
        else:
            return {"error": "扫描无输出", "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"error": "扫描超时（超过120秒）"}
    except Exception as e:
        return {"error": str(e)}