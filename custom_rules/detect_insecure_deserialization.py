import bandit
from bandit.core import test_properties as test

@test.checks('Call')
@test.test_id('B998')
def detect_unsafe_pickle_loads(context):
    """检测不安全的 pickle.load() / pickle.loads() / cPickle 调用"""
    call_name = context.call_function_name_qual
    if call_name in ('pickle.load', 'pickle.loads', 'cPickle.load', 'cPickle.loads'):
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.HIGH,
            text="[B998] 不安全的 pickle 反序列化调用。禁止反序列化不可信数据！"
        )

@test.checks('Call')
@test.test_id('B999')
def detect_unsafe_yaml_load(context):
    """检测不安全的 yaml.load() 调用（无 SafeLoader）"""
    call_name = context.call_function_name_qual
    # 匹配 yaml.load 以及 yaml.unsafe_load
    if call_name in ('yaml.load', 'yaml.unsafe_load'):
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.MEDIUM,
            text="[B999] 不安全的 YAML 反序列化调用。请使用 yaml.safe_load()！"
        )