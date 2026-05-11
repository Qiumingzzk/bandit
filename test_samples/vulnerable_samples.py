import pickle
import yaml
import joblib
import numpy as np

def unsafe_pickle(data):
    obj = pickle.loads(data)  # vulnerability

def unsafe_yaml(data):
    obj = yaml.load(data)     # vulnerability

def unsafe_joblib(path):
    model = joblib.load(path) # vulnerability

def unsafe_numpy(path):
    arr = np.load(path, allow_pickle=True)  # vulnerability