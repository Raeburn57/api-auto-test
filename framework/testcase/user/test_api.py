import os, pytest, jsonpath
from common.yaml_util import YamlUtil
from common.request_util import RequestUtil
from common.assertion_util import AssertionUtils
from common.variable_util import ExtractUtil, GlobalVariableUtil, VariableReplaceUtil
from common.file_util import FileUtil
from common.path_util import TESTCASE_DIR
from common.global_config import GLOBAL_CONFIG
from testcase.user.biz_hooks import UserHooks
import allure


testcase_path = os.path.join(TESTCASE_DIR, "user/test_api.yaml")
class TestAPI:

    @pytest.fixture(scope="module", autouse=True)
    def run_module_hooks(self):
        with allure.step("【模块前置】初始化模块环境"):
            UserHooks.setup()
        yield

        with allure.step("【模块后置】清理模块环境"):
            UserHooks.teardown()

    @pytest.mark.parametrize("case_data", YamlUtil.read_testcase(testcase_path))
    def test_user(self, case_data):

        host = GLOBAL_CONFIG["host"]
        basic_info = case_data["basic_info"]
        testcase = case_data["testcase"]
        case_name = testcase.get("case_name", "未命名的测试用例")
        print(basic_info["api_name"])
        print(testcase["case_name"])

        allure.dynamic.title(case_name)

        # 用例前置
        with allure.step("【用例前置】初始化用例环境"):
            case_setup = testcase.get("setup", [])
            if case_setup:
                for setup_name in case_setup:
                    if not hasattr(UserHooks, setup_name):
                        raise RuntimeError(
                            f"{setup_name} 未在biz_hooks配置"
                        )
                    method = getattr(UserHooks, setup_name)
                    method()

        # 获取接口请求参数
        with allure.step("【解析接口请求参数与变量替换】"):
            content_type = basic_info["content_type"]
            method = basic_info["method"]
            url = host + basic_info["url"]
            headers = basic_info.get("headers")
            request_data = testcase.get("data")
            file_name = testcase.get("file_name")

            # 变量替换
            if headers:
                headers = VariableReplaceUtil.replace_var(headers)
            if request_data:
                request_data = VariableReplaceUtil.replace_var(request_data)

            # 初始化请求参数
            params = None
            data = None
            json_data = None
            files = None

            # 按用例文件定义的传参类型构造接口请求参数
            if content_type == "application/json":
                json_data = request_data

            elif content_type == "application/x-www-form-urlencoded":
                data = request_data

            elif content_type == "multipart/form-data":
                data = request_data
                if file_name:
                    files = {"file": FileUtil.get_file_stream(file_name)}

            elif content_type == "file":
                if file_name:
                    files = {"file": FileUtil.get_file_stream(file_name)}

            elif content_type == "text/plain":
                data = request_data

            elif content_type == "query":
                params = request_data

        # 接口请求
        with allure.step("【发送请求】"):
            response = RequestUtil().send_request(
                method = method,
                url = url,
                headers = headers,
                params = params,
                data = data,
                json = json_data,
                files = files
            )

        # 响应断言
        with allure.step("【接口响应断言】"):
            api_validate = testcase.get("api_validate", [])
            AssertionUtils.assert_resp(response, api_validate)

        # 提取变量
        with allure.step("【提取变量】"):
            extracts = testcase.get("extracts", [])
            if extracts:
                extract_map = ExtractUtil.extract_resp_var(response, extracts)
                GlobalVariableUtil.set_global_vars(extract_map)
                GlobalVariableUtil.show_global_vars()

        # 数据库校验
        with allure.step("【数据库校验】"):
            db_validate = testcase.get("db_validate", [])
            AssertionUtils.assert_db(db_validate)

        # 用例后置
        with allure.step("【用例后置】清理用例环境"):
            case_teardown = testcase.get("teardown", [])
            if case_teardown:
                for teardown_name in case_teardown:
                    if not hasattr(UserHooks, teardown_name):
                        raise RuntimeError(
                            f"{teardown_name} 未在biz_hooks配置"
                        )
                    method = getattr(UserHooks, teardown_name)
                    method()

