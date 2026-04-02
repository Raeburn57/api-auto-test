class UserHooks:
    @staticmethod
    def setup():
        print("用户模块前置操作")
        UserHooks.creat_user()

    @staticmethod
    def teardown():
        print("用户模块后置操作")
        UserHooks.delete_user()


    @staticmethod
    def creat_user():
        print("创建用户")

    @staticmethod
    def delete_user():
        print("注销用户")

    @staticmethod
    def case_setup1():
        print("用例前置测试1")

    @staticmethod
    def case_setup2():
        print("用例前置测试2")

    @staticmethod
    def case_teardown1():
        print("用例后置测试1")