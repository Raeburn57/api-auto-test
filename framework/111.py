import json

import pytest

# from common.yaml_util import YamlUtil
# from common.variable_util import VariableReplaceUtil, GlobalVariableUtil
#
#
# case_data = YamlUtil.read_testcase("./testcase/user/test_api.yaml")
# testcase = case_data[0]["testcase"]
# print(testcase)
# db_validate = testcase["db_validate"]
# db_validate = VariableReplaceUtil.replace_var(db_validate)
# print(db_validate)
#
# GlobalVariableUtil.clear_global_var("userId")
# GlobalVariableUtil.show_global_vars()


# import re
# a = "${test}"
# comp = re.compile(r"\$\{(\w+)}")
# print(comp)
# b = re.sub(comp, "aaaa", a)
# print(b)

a = ['a', 'b', 'c']
x = "\n".join(a)
print(x)


# a = {"eq": ["code", 0]}
# print(next(iter(a.items())))


# print(YamlUtil.read_testcase('test_api.yaml'))



# validate_rules = [{"eq": ["code", 0]}, {"eq": ["type", "a"]}]
# for rule in validate_rules:
#     print(rule)
#     print(rule.items())
#     assert_type, condition = next(iter(rule.items()))
#     assert_field, asert_value = condition
#     print(assert_type, assert_field, asert_value)


# a = {"b":1, "c":2}
# for k, v in a.items():
#     print(k, v)


# resp = {
#     "users": [
#         {"name": "张三", "age": 20},
#         {"name": "李四", "age": 25}
#     ]
# }
#
# path = "$.users[1].name"
# from jsonpath_ng import parse
# print(parse(path))
# print(parse(path).find(resp))
# print(parse(path).find(resp)[0])
# print(parse(path).find(resp)[0].value)


# dict = {
#     "users": [
#         {"name": "张三", "age": 20},
#         {"name": "李四", "age": 25}
#     ],
#     "a": "测试",
#     "b": "xxx"
# }
#
# def clear_variable(dict, key):
#     dict.pop(key, None)
    # print(dict)

# print(dict.keys())
# clear_variable(dict, "a")
# clear_variable(dict, "c")

# print(clear_variable(dict, "c"))


# base_uri = 'https://test12.ys7.com'
#
# class TestAPI:
#     @pytest.mark.parametrize("case_data", YamlUtil.read_yaml("./test_api.yaml"))
#     def login_c(self, base_url, case_data):
#         print(case_data)
#
# TestAPI.login_c()
# from common.assertion_util import AssertionUtils
# case_data = YamlUtil.read_yaml("./test_api.yaml")
# print(case_data[0])
# print(AssertionUtils.get_field_value(case_data[0], "$.basicInfo.api_name"))



