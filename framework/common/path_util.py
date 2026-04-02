import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_DIR = os.path.join(ROOT_DIR, "config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")

DATA_DIR = os.path.join(ROOT_DIR, "data")

TESTCASE_DIR = os.path.join(ROOT_DIR, "testcase")