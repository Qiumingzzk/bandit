import pytest
import bandit.core.config
import bandit.core.manager
import os

def run_bandit_on_file(file_path):
    config = bandit.core.config.BanditConfig()
    manager = bandit.core.manager.BanditManager(config=config, agg_type='vuln')
    manager.discover_files([file_path], recursive=False)
    manager.run_tests()
    return manager.get_issue_list()

def test_vulnerable_sample():
    path = os.path.join(os.path.dirname(__file__), '../test_samples/vulnerable_sample.py')
    issues = run_bandit_on_file(path)
    assert len(issues) >= 3, f"Expected at least 3 issues, got {len(issues)}"

def test_secure_sample():
    path = os.path.join(os.path.dirname(__file__), '../test_samples/secure_sample.py')
    issues = run_bandit_on_file(path)
    assert len(issues) == 0, f"Secure sample should have 0 issues, got {len(issues)}"