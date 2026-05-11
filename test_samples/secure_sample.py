import yaml
import pickle

# 使用安全方法
safe_yaml = yaml.safe_load("{name: John}")
# 正常使用 pickle.dumps 不触发检测
data = pickle.dumps({"a": 1})