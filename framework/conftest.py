import pytest
from common.path_util import CONFIG_PATH
from common.global_config import GLOBAL_CONFIG
from common.yaml_util import YamlUtil
from common.yaml_util import clear_yaml
from common.global_hooks import GlobalHooks

# 注册命令行参数“--env”
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        default="test12",
        help="环境参数：test12/prod"
    )

# 加载全局配置
@pytest.fixture(scope="session", autouse=True)
def load_global_config(request):
    # 从命令行获取env参数
    env = request.config.getoption("--env")
    all_config = YamlUtil.read_yaml(CONFIG_PATH)
    if env not in all_config:
        raise ValueError(
            f'传入环境"{env}"未配置！\n'
            f'当前已配置的环境：{list(all_config.keys())}'
        )
    GLOBAL_CONFIG.update(all_config[env])

# 执行项目前后置
@pytest.fixture(scope="session", autouse=True)
def do_global_hooks():
    GlobalHooks.setup()
    yield
    GlobalHooks.teardown()

# 标记用例tag
def pytest_collection_modifyitems(config, items):
    marker_list = config.getini("markers")
    allowed_tags = set()

    for marker in marker_list:
        tag_name = marker.split(":")[0].strip()
        allowed_tags.add(tag_name)

    for item in items:
        case_data = item.callspec.params.get("case_data")
        if not case_data:
            continue

        test_case = case_data.get("testcase", {})
        yaml_tags = test_case.get("tags", [])

        for yaml_tag in yaml_tags:
            if yaml_tag in allowed_tags:
                item.add_marker(getattr(pytest.mark, yaml_tag))


# @pytest.fixture(scope="session")
# def env(request):
#     return request.config.getoption("--env")

# fixture作用域：function、class、module、package、session
# @pytest.fixture(scope = "package", autouse = True)
# def opts():
#     print("执行前置操作")
#     yield
#     print("执行后置操作")

# @pytest.fixture(scope = "class", autouse = True, params = [["param1", "value1"], ["param2", "value2"], ["param3", "value3"]], name = "fixture参数化测试")
# def get_params(request):
#     print("fixture参数化前置操作")
#     yield request.param
#     print("fixture参数化后置操作")

# 清空yaml
@pytest.fixture(scope = "session", autouse = True)
def clears():
    clear_yaml()

