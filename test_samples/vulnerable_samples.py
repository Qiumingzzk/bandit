import yaml
import pickle
import os

# 不安全 YAML 反序列化 (应被 B999 检测)
data = yaml.load("!!python/object/apply:os.system ['ls']")

# 不安全 Pickle 反序列化 (应被 B998 检测)
payload = pickle.loads(b"cos\nsystem\n(S'echo vulnerable'\ntR.")

# 安全代码（不应告警）
safe_data = yaml.safe_load("{name: John}")