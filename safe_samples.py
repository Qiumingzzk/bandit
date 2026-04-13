# safe_samples.py
import os
from cryptography.fernet import Fernet

API_KEY = os.environ.get("API_KEY")  # 安全：从环境变量获取
key = Fernet.generate_key()  # 安全：动态生成
cipher = Fernet(key)  # 安全：强加密

def hash_password(pwd):
    import hashlib
    salt = os.urandom(32)
    return hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)  # 安全：强哈希