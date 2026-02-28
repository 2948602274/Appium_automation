import pytest as pytest
import os
from allure_combine import combine_allure



# 确定这几个步骤

args = [
    '-vs', '--capture=sys',  # 日志信息更加信息 固定代码
    '--clean-alluredir',     # 清空测试数据每次都是最新的数据 固定
    '--alluredir=allure-results',  # --alluredir=生成测试数据文件夹 allure-results可以变 不建议变
    './HAT/core/TestRunner.py'     # 执行用例的文件位置
]

pytest.main(args)  # 执行用例

# 生成测试报告 allure-report可以变 不建议变
os.system('allure generate -c -o allure-report')

# 测试报告只能在pycharm里面打开 不能在本地打开 想着本地打开
# 安装allure_combine  complete.html在本地打开
combine_allure('allure-report')




# if __name__ == '__main__':
#     pytest.main(['-vs',r'D:\appium_test\HAT\core\TestRunner.py'])