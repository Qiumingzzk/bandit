import subprocess
import json
from pathlib import Path

def test_bandit_plugin_detects_vulnerabilities():
    """测试自定义插件能检出漏洞样本"""
    root = Path(__file__).parent.parent
    target = root / 'test_samples' / 'vulnerable_sample.py'
    cmd = [
        'bandit', str(target),
        '-p', 'custom_rules.detect_insecure_deserialization',
        '-f', 'json', '--quiet'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Bandit 发现漏洞时返回非0
    assert result.returncode != 0, "应该检测到漏洞但未检出"
    data = json.loads(result.stdout)
    issue_ids = [issue['test_id'] for issue in data.get('results', [])]
    assert 'B998' in issue_ids or 'B999' in issue_ids, "未检测到自定义规则问题"

def test_bandit_plugin_ignores_secure_code():
    """测试安全样本不应产生告警"""
    root = Path(__file__).parent.parent
    target = root / 'test_samples' / 'secure_sample.py'
    cmd = [
        'bandit', str(target),
        '-p', 'custom_rules.detect_insecure_deserialization',
        '-f', 'json', '--quiet'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # 无漏洞时返回0
    assert result.returncode == 0, "安全代码误报"