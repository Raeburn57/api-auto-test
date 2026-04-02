import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pytest
import os
from common.path_util import TESTCASE_DIR

if __name__ == '__main__':
    os.makedirs("report", exist_ok=True)

    args = [
        TESTCASE_DIR, # 用例路径
        "-m=smoke",
        "-vs",
        "--html=./report/report.html",
        "--self-contained-html",
        "--alluredir=report/allure_data",
        "--clean-alluredir",
        "--env=test12"
    ]

    pytest.main(args)