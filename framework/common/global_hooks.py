from common.db_util import DBUtil

class GlobalHooks:
    @staticmethod
    def setup():
        print("项目前置操作")
        GlobalHooks.global_setup1()

    @staticmethod
    def teardown():
        DBUtil.db_close()
        print("项目后置操作")


    @staticmethod
    def global_setup1():
        print("全局前置操作1")