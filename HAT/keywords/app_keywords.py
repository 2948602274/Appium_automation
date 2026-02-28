from appium import webdriver
import allure
from HAT.core.globalContext import g_context
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Keywords:
    def __init__(self,driver):
        self.driver=driver
        # cap = {
        #     "platformName": "Android",
        #     "platformVersion": "12",
        #     "deviceName": "127.0.0.1:7555",
        #     "appPackage": "uni.UNI2317D55",
        #     "appActivity": "io.dcloud.uniapp.UniAppActivity",
        #     "noReset": True,
        #     "unicodeKeyboard": True,
        #     "resetKeyboard": True,
        #     "automationName": "UiAutomator2"
        # }
        # options = UiAutomator2Options().load_capabilities(cap)
        #
        # self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    @allure.step("等待元素出现")
    def wait_for_element_presence(self, locator):
        try:
            els=WebDriverWait(self.driver,3).until(EC.presence_of_all_elements_located(locator))
            return els
        except Exception as e:
            print("未找到元素")
            return False

    @allure.step("查找元素")
    def find_else(self,**kwargs):
        locator_types = {
            'id': AppiumBy.ID,
            'xpath': AppiumBy.XPATH,
            'class_name': AppiumBy.CLASS_NAME,
            'name': AppiumBy.NAME,
            'css_selector': AppiumBy.CSS_SELECTOR,
            'link_text': AppiumBy.LINK_TEXT,
            'partial_link_text': AppiumBy.PARTIAL_LINK_TEXT,
            'tag_name': AppiumBy.TAG_NAME,
            'AppiumBy.XPATH': AppiumBy.XPATH,
        }
        key=str(kwargs['页面元素'])
        all_ele_data=g_context().get_dict('APP页面')
        ele_data=all_ele_data(key)
        locator_types = locator_types.get(ele_data['type'], None)
        locator = (locator_types, ele_data['value'])
        elses_list=self.wait_for_element_presence(locator)
        if len(elses_list)==1:
            return elses_list[0]
        else:
            index=int(kwargs.get("INDEX",0))
            return elses_list[index]

    @allure.step("点击元素")
    def click_element(self,**kwargs):
        else_list=self.find_else(**kwargs)
        else_list.click()

    @allure.step("输入文本")
    def input_text(self,**kwargs):
        else_list=self.find_else(**kwargs)
        else_list.send_keys(kwargs['text'])