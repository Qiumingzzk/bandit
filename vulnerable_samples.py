# vulnerable_samples.py
API_KEY = "sk-live-8a9b7c6d5e4f3g2h1i0j"  # 应检出
DATABASE_PASSWORD = "Admin@123"  # 应检出
config = {"aws_secret": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}  # 应检出
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # 应检出（高熵）

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123"  # 应检出
    )

import hashlib
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()  # 应检出（弱哈希）