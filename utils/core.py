class MyResponse():
    def __init__(self):
        self.code = 200
        self.msg = "执行成功"

    @property
    def get_dic(self):
        return self.__dict__