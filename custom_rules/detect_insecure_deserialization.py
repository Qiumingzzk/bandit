import ast
import bandit
from bandit.core import test_properties as test

@test.checks('Call')
def detect_insecure_deserialization(context):
    """检测不安全反序列化调用（pickle, yaml, joblib, numpy）"""
    node = context.node
    # 提取函数名
    if isinstance(node.func, ast.Attribute):
        if isinstance(node.func.value, ast.Name):
            func_name = f"{node.func.value.id}.{node.func.attr}"
        else:
            func_name = node.func.attr
    elif isinstance(node.func, ast.Name):
        func_name = node.func.id
    else:
        return

    # 危险函数列表
    if func_name in ('pickle.load', 'pickle.loads'):
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.HIGH,
            text=f"Insecure deserialization: {func_name} may lead to RCE. Do not load untrusted data."
        )
    if func_name == 'yaml.load':
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.HIGH,
            text="yaml.load with default loader is unsafe. Use yaml.safe_load instead."
        )
    if func_name == 'joblib.load':
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.HIGH,
            text="joblib.load is based on pickle, unsafe for untrusted data."
        )
    if func_name == 'numpy.load':
        for kw in node.keywords:
            if kw.arg == 'allow_pickle' and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                return bandit.Issue(
                    severity=bandit.MEDIUM,
                    confidence=bandit.HIGH,
                    text="numpy.load with allow_pickle=True may allow arbitrary code execution."
                )
    return