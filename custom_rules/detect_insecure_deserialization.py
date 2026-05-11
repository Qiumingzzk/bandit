import bandit
from bandit.core import test_properties as test


@test.test_plugin('detect_insecure_deserialization')
def detect_insecure_deserialization(context):
    """检测不安全反序列化调用"""
    import ast
    call_node = context.node
    if not isinstance(call_node, ast.Call):
        return None

    # 提取函数名
    func = call_node.func
    if isinstance(func, ast.Attribute):
        if isinstance(func.value, ast.Name):
            full_name = f"{func.value.id}.{func.attr}"
        else:
            full_name = func.attr
    elif isinstance(func, ast.Name):
        full_name = func.id
    else:
        return None

    # 危险函数列表
    if full_name in ('pickle.load', 'pickle.loads', 'yaml.load', 'joblib.load'):
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.HIGH,
            text=f"Insecure deserialization: {full_name}. Do not deserialize untrusted data."
        )
    # numpy.load 特殊处理
    if full_name == 'numpy.load':
        for kw in call_node.keywords:
            if kw.arg == 'allow_pickle' and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                return bandit.Issue(
                    severity=bandit.MEDIUM,
                    confidence=bandit.HIGH,
                    text="numpy.load with allow_pickle=True is unsafe."
                )
    return None