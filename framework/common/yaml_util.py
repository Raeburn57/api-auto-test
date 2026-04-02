import os
import yaml


# 写入yaml
def write_yaml(data):
    with open(os.getcwd() + "/extract.yaml", encoding = "utf-8", mode = "a+") as f:
        yaml.dump(data, stream = f, allow_unicode = True)

# 读取yaml
def read_yaml(key):
    with open(os.getcwd() + "/extract.yaml", encoding = "utf-8", mode = "r") as f:
        value = yaml.safe_load(f)
        return value[key]

# 清空yaml
def clear_yaml():
    with open(os.getcwd() + "/extract.yaml", encoding = "utf-8", mode = "w") as f:
        f.truncate()

# 读取测试用例



class YamlUtil:

    @staticmethod
    def read_yaml(path):
        with open(path, encoding="utf-8", mode="r") as f:
            value = yaml.safe_load(f)
            return value

    @staticmethod
    def write_yaml(data):
        with open(data, encoding="utf-8", mode="w") as f:
            yaml.dump(data, f, allow_unicode = True)

    @staticmethod
    def read_testcase(path):
        api_list = YamlUtil.read_yaml(path)
        all_cases = []

        for api in api_list:
            basic_info = api["basicInfo"]
            testcases = api.get("testcases", [])

            for testcase in testcases:
                full_case = {"basic_info": basic_info, "testcase": testcase}
                all_cases.append(full_case)

        return all_cases







