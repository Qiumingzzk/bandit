import sys
import ast

def scan_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return []

    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            # 获取完整函数名
            if isinstance(func, ast.Attribute):
                if isinstance(func.value, ast.Name):
                    full_name = f"{func.value.id}.{func.attr}"
                else:
                    full_name = func.attr
            elif isinstance(func, ast.Name):
                full_name = func.id
            else:
                continue

            # 危险函数检查
            if full_name in ('pickle.load', 'pickle.loads', 'yaml.load', 'joblib.load'):
                issues.append((node.lineno, full_name, "HIGH"))
            elif full_name == 'numpy.load':
                for kw in node.keywords:
                    if kw.arg == 'allow_pickle' and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        issues.append((node.lineno, full_name, "MEDIUM"))
    return issues

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scan_standalone.py <python_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    issues = scan_file(file_path)
    if issues:
        print(f"\n[!] Found {len(issues)} potential insecure deserialization issue(s) in {file_path}:\n")
        for line, name, severity in issues:
            print(f"  Line {line:4d} [{severity}] {name}")
    else:
        print(f"\n[+] No insecure deserialization issues found in {file_path}.")