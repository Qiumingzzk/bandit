import os
import ast
import json

def run_bandit_scan(target_path: str):
    """自实现 AST 扫描，返回与 Bandit 兼容的 JSON 格式"""
    if not os.path.exists(target_path):
        return {"error": f"Path does not exist: {target_path}"}

    issues = []
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
    except (SyntaxError, UnicodeDecodeError, FileNotFoundError) as e:
        return {"error": f"Failed to parse file: {e}", "results": []}

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            # 提取完整函数名
            if isinstance(func, ast.Attribute):
                if isinstance(func.value, ast.Name):
                    full_name = f"{func.value.id}.{func.attr}"
                else:
                    full_name = func.attr
            elif isinstance(func, ast.Name):
                full_name = func.id
            else:
                continue

            # 危险函数检测
            if full_name in ('pickle.load', 'pickle.loads'):
                issues.append({
                    "test_name": "detect_insecure_deserialization",
                    "test_id": "B999",
                    "severity": "HIGH",
                    "confidence": "HIGH",
                    "line_number": node.lineno,
                    "line_range": [node.lineno],
                    "filename": target_path,
                    "issue_text": f"Insecure deserialization: {full_name} may lead to RCE. Do not load untrusted data.",
                    "issue_cwe": {"id": 502, "link": "https://cwe.mitre.org/data/definitions/502.html"},
                    "issue_severity": "HIGH"
                })
            elif full_name == 'yaml.load':
                issues.append({
                    "test_name": "detect_insecure_deserialization",
                    "test_id": "B999",
                    "severity": "MEDIUM",
                    "confidence": "HIGH",
                    "line_number": node.lineno,
                    "line_range": [node.lineno],
                    "filename": target_path,
                    "issue_text": "yaml.load with default loader is unsafe. Use yaml.safe_load instead.",
                    "issue_cwe": {"id": 502},
                    "issue_severity": "MEDIUM"
                })
            elif full_name == 'joblib.load':
                issues.append({
                    "test_name": "detect_insecure_deserialization",
                    "test_id": "B999",
                    "severity": "MEDIUM",
                    "confidence": "HIGH",
                    "line_number": node.lineno,
                    "line_range": [node.lineno],
                    "filename": target_path,
                    "issue_text": "joblib.load is based on pickle, unsafe for untrusted data.",
                    "issue_cwe": {"id": 502},
                    "issue_severity": "MEDIUM"
                })
            elif full_name == 'numpy.load':
                # 检查 allow_pickle 参数
                allow_pickle = False
                for kw in node.keywords:
                    if kw.arg == 'allow_pickle' and isinstance(kw.value, ast.Constant):
                        allow_pickle = kw.value.value
                if allow_pickle:
                    issues.append({
                        "test_name": "detect_insecure_deserialization",
                        "test_id": "B999",
                        "severity": "MEDIUM",
                        "confidence": "HIGH",
                        "line_number": node.lineno,
                        "line_range": [node.lineno],
                        "filename": target_path,
                        "issue_text": "numpy.load with allow_pickle=True may allow arbitrary code execution.",
                        "issue_cwe": {"id": 502},
                        "issue_severity": "MEDIUM"
                    })

    # 构造 Bandit 兼容的输出结构
    output = {
        "results": issues,
        "errors": [],
        "metrics": {
            "totals": {
                "SEVERITY": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
                "CONFIDENCE": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            }
        }
    }
    # 统计
    for issue in issues:
        sev = issue["severity"]
        output["metrics"]["totals"]["SEVERITY"][sev] = output["metrics"]["totals"]["SEVERITY"].get(sev, 0) + 1
        conf = issue["confidence"]
        output["metrics"]["totals"]["CONFIDENCE"][conf] = output["metrics"]["totals"]["CONFIDENCE"].get(conf, 0) + 1

    return output