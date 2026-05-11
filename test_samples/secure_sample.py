import json
import yaml
import numpy as np

def safe_pickle(data):
    obj = json.loads(data)   # safe

def safe_yaml(data):
    obj = yaml.safe_load(data)  # safe

def safe_joblib(path):
    with open(path.replace('.pkl', '.json'), 'r') as f:
        model = json.load(f)

def safe_numpy(path):
    arr = np.load(path, allow_pickle=False)  # safe