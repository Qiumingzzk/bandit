编码规范
（1）代码风格规范
缩进：4个空格，禁止使用Tab。
行宽：不超过120字符。
命名规则：
类名：PascalCase（如 User, ScanTask）
函数/方法名：snake_case（如 create_app, run_bandit_scan）
常量：UPPER_SNAKE_CASE（如 DANGEROUS_CALLS）
私有成员：前缀单下划线 _internal_func
注释：复杂函数必须包含docstring（描述参数、返回值、异常）。
（2）代码设计规范
单一职责：每个函数只做一件事。例如 run_bandit_scan 只负责调用Bandit，不处理数据库写入。
依赖倒置：业务逻辑依赖抽象接口（如使用SQLAlchemy的模型基类）。
异常处理：统一捕获顶级异常，记录日志并返回500错误，避免泄露敏感信息。
日志规范：
INFO：记录用户登录、扫描任务创建/完成。
ERROR：记录数据库连接失败、Bandit调用异常。
禁止在日志中打印密码、令牌等敏感数据。