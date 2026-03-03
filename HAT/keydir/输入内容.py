import allure
from HAT.keywords.app_keywords import Keywords

class 输入内容(Keywords):
    def __init__(self,driver):
        self.driver=driver

    @allure.step("输入内容")
    def 输入内容(self,**kwargs):
        else_list=self.find_else(**kwargs)
        else_list.send_keys(kwargs['数据内容'])
