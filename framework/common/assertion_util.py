import json, jsonpath_ng, pytest
from common.variable_util import VariableReplaceUtil, ExtractUtil
from common.db_util import DBUtil
import allure

class SoftAssert:
    def __init__(self):
        self.failures = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.failures:
            failure_message = '\n------------------------------------------\n'.join(self.failures)
            allure.attach(
                failure_message,
                name = "断言失败详情",
                attachment_type = allure.attachment_type.TEXT
            )
            raise AssertionError(
                f'检出{len(self.failures)}处断言失败：\n{failure_message}'
            )

        return True

    def add_failure(self, failure_message):
        self.failures.append(failure_message)


class AssertionUtils:

    @staticmethod
    def do_assert(assert_type, assert_field, response_value, expected_value):
        assert_descs = {
            "eq": "等于",
            "ne": "不等于",
            "gt": "大于",
            "lt": "小于",
            "gte": "大于等于",
            "lte": "小于等于",
            "in": "包含于",
            "contains": "包含",
            "not_null": "不为空",
            "is_null": "为空",
            "startswith": "开头是",
            "endswith": "结尾是",
            "len_eq": "长度等于",
            "len_gt": "长度大于",
            "len_lt": "长度小于"
        }
        assert_desc = assert_descs.get(assert_type, assert_type)

        if assert_type in ["not_null", "is_null"]:
            err_msg = (f'校验失败！【{assert_field}】应当{assert_desc}，\n'
                       f'实际结果：【{response_value}】')

        else:
            err_msg = (f'校验失败！【{assert_field}】应当{assert_desc} 【{expected_value}】，\n'
                       f'实际结果：【{response_value}】')

        try:
            if assert_type == 'eq':
                is_pass =  response_value == expected_value
            elif assert_type == 'ne':
                is_pass =  response_value != expected_value
            elif assert_type == 'gt':
                is_pass =  response_value > expected_value
            elif assert_type == 'lt':
                is_pass =  response_value < expected_value
            elif assert_type == 'gte':
                is_pass =  response_value >= expected_value
            elif assert_type == 'lte':
                is_pass =  response_value <= expected_value
            elif assert_type == 'in':
                is_pass =  str(response_value) in str(expected_value)
            elif assert_type == 'contains':
                is_pass =  str(expected_value) in str(response_value)
            elif assert_type == 'not_null':
                is_pass =  response_value is not None and response_value != ''
            elif assert_type == 'is_null':
                is_pass =  response_value is None or response_value == ''
            elif assert_type == 'startswith':
                is_pass =  str(response_value).startswith(str(expected_value))
            elif assert_type == 'endswith':
                is_pass =  str(response_value).endswith(str(expected_value))
            elif assert_type == 'len_eq':
                is_pass =  len(response_value) == expected_value
            elif assert_type == 'len_gt':
                is_pass =  len(response_value) > expected_value
            elif assert_type == 'len_lt':
                is_pass =  len(response_value) < expected_value
            else:
                raise NotImplementedError(
                    f'不支持的断言类型：{assert_type}'
                )

            return is_pass, err_msg

        except Exception as e:
            return False, f'断言执行异常：{str(e)}'


    @staticmethod
    def assert_resp(response, validate_rules:list):
        if not hasattr(response, 'json'):
            raise TypeError(
                '参数"response"非法！'
            )

        if not validate_rules:
            print('⚠ 当前用例未配置响应断言，已跳过校验！')
            return

        try:
            resp_data = response.json()
        except json.JSONDecodeError:
            raise Exception(
                f'接口响应非JSON格式，不支持断言！HTTP状态码：{response.status_code}\n'
                f'接口响应内容：{response.text}'
            )

        validate_rules = VariableReplaceUtil.replace_var(validate_rules)

        with SoftAssert() as soft_assert:
            for rule in validate_rules:
                validate_type, condition = next(iter(rule.items()))

                if validate_type in ["is_null", "not_null"]:
                    assert_field = condition[0]
                    assert_value = None
                else:
                    assert_field, assert_value = condition

                if assert_field == 'status_code':
                    resp_value = response.status_code
                else:
                    resp_value = ExtractUtil.get_field_value(resp_data, assert_field)

                is_success, err_msg = AssertionUtils.do_assert(validate_type, assert_field, resp_value, assert_value)

                if not is_success:
                    soft_assert.add_failure(err_msg)

    @staticmethod
    def assert_db(db_validate:list):
        if not db_validate:
            print('⚠ 当前用例未配置数据库断言，已跳过校验！')
            return

        with SoftAssert() as soft_assert:
            for item in db_validate:
                sql = item.get("sql")
                validate_rules = item.get("validate")

                if not validate_rules or not sql:
                    print(
                        f'⚠ 数据库校验对象"{item}"配置不全，缺少sql或校验规则！'
                    )
                    continue

                sql = VariableReplaceUtil.replace_var_with_text(sql)
                db_data = DBUtil.db_query_one(sql)

                for rule in validate_rules:
                    validate_type, condition = next(iter(rule.items()))

                    if validate_type in ["is_null", "not_null"]:
                        assert_field = condition[0]

                        if not assert_field.startswith("db_"):
                            raise ValueError(
                                f'{assert_field}命名不合规，请以“db_”开头'
                            )

                        db_field = assert_field[3:]

                    else:
                        assert_field, db_field = condition
                        if not db_field.startswith("db_"):
                            raise ValueError(
                                f'{db_field}命名不合规，请以“db_”开头'
                            )
                        db_field = db_field[3:]

                    acture_value = VariableReplaceUtil.replace_var(assert_field)
                    db_value = db_data.get(db_field, "null")

                    is_success, err_msg = AssertionUtils.do_assert(
                        validate_type,
                        assert_field,
                        acture_value,
                        db_value
                    )

                    if not is_success:
                        soft_assert.add_failure(err_msg)





    # @staticmethod
    #
    #
    # @staticmethod
    # def assert_json(response, json_rules):
    #     response_json = response.json()
    #     for key_path, expected_value in json_rules.items():
    #         # 支持嵌套字段路径（如 "data.userId"）
    #         keys = key_path.split('.')
    #         actual = response_json
    #         for k in keys:
    #             actual = actual.get(k, {})
    #         assert actual == expected_value, \
    #             f"字段 {key_path} 预期值 {expected_value}，实际为 {actual}"


# from responses_validator import validator
#
# resp = None
# validator(
#     resp,
#     status_code=200,
#     text= '',
#     json= {
#
#     }
# )

