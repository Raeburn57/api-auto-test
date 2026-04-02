import json, jsonpath_ng
import re

from common.global_config import GLOBAL_CONFIG


class GlobalVariableUtil:

    global_variables = {}

    @classmethod
    def set_global_var(cls, key, value):
        cls.global_variables[key] = value

    @classmethod
    def set_global_vars(cls, extract_map):
        if not isinstance(extract_map, dict):
            raise TypeError(
                '参数"global_vars"必须是字典格式!'
            )

        for k, v in extract_map.items():
            if k in cls.global_variables:
                print(f'⚠ 全局变量：{k} 已被覆盖，原值：{cls.global_variables[k]}，新值：{v}')
        cls.global_variables.update(extract_map)


    @classmethod
    def get_global_var(cls, key):
        if key not in cls.global_variables:
            raise KeyError(
                f'全局变量"{key}"不存在！'
            )
        return cls.global_variables[key]

    @classmethod
    def clear_global_var(cls, key):
        cls.global_variables.pop(key)

    @classmethod
    def show_global_vars(cls):
        print("当前全局变量：", cls.global_variables)



class ExtractUtil:

    @staticmethod
    def get_field_value(data, field_path):

        try:
            path_parse = jsonpath_ng.parse(field_path)
            matches = path_parse.find(data)

            if matches:
                value = matches[0].value
            else:
                value = None
            return value

        except (AttributeError, IndexError):
            return None

    @staticmethod
    def extract_resp_var(response, extracts:list):

        if not hasattr(response, 'json'):
            raise TypeError(
                '参数"response"非法！'
            )

        try:
            response_data = response.json()
        except json.JSONDecodeError:
            raise Exception(
                '接口响应非JSON格式，不支持提取！\n'
                f'接口响应内容：{response.text}'
            )

        extract_map = {}

        for extract in extracts:
            field, field_path_list = next(iter(extract.items()))
            field_path = field_path_list[0]
            value = ExtractUtil.get_field_value(response_data, field_path)
            extract_map[field] = value

        return extract_map


class VariableReplaceUtil:

    @staticmethod
    def replace_var(data):

        if isinstance(data, dict):
            new_data = {}
            for k, v in data.items():
                new_data[k] = VariableReplaceUtil.replace_var(v)
            return new_data

        elif isinstance(data, list):
            new_list = []
            for item in data:
                new_item = VariableReplaceUtil.replace_var(item)
                new_list.append(new_item)
            return new_list

        elif isinstance(data, str):
            s = data.strip()
            # 处理全局变量
            if s.startswith("${") and s.endswith("}"):
                key = s[2:-1]
                return GlobalVariableUtil.get_global_var(key)

            # 处理环境常量
            elif s.startswith("{{") and s.endswith("}}"):
                key = s[2:-2]
                return GLOBAL_CONFIG.get(key, data)

        return data



    @staticmethod
    def replace_var_with_text(text: str):
        if not isinstance(text, str):
            raise TypeError(
                f'数据替换失败：入参必须为字符串！'
            )

        pattern_global = re.compile(r"\$\{(\w+)}")
        text_replaced_global = pattern_global.sub(VariableReplaceUtil._replace_global_var, text)

        pattern_env = re.compile(r"\{\{(\w+)}}")
        text_final = pattern_env.sub(VariableReplaceUtil._replace_env_var, text_replaced_global)

        return text_final

    @staticmethod
    def _replace_global_var(match):
        var_name = match.group(1)

        if var_name not in GlobalVariableUtil.global_variables:
            raise KeyError(
                f'替换失败！全局变量：{var_name} 不存在！'
            )

        value = GlobalVariableUtil.global_variables[var_name]
        return str(value)

    @staticmethod
    def _replace_env_var(match):
        var_name = match.group(1)

        if var_name not in GLOBAL_CONFIG:
            raise KeyError(
                f'替换失败！全局变量：{var_name} 不存在！'
            )

        value = GLOBAL_CONFIG[var_name]
        return str(value)








