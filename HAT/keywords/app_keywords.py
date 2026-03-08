import allure
import sys
from HAT.core.globalContext import g_context
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
        self.截图()

    @allure.step("输入文本")
    def input_text(self,**kwargs):
        else_list=self.find_else(**kwargs)
        else_list.send_keys(kwargs['text'])

    def ex_invoke(self,**kwargs):
        key=kwargs['key']
        sys.path.append(g_context().get_dict("key_dir"))
        __import__(key)
        module=__import__(key)
        class_=getattr(module,key)
        key_func=class_(self.driver).__getattribute__(key)
        key_func(**kwargs["step_value"])

    @allure.step("截图")
    def 截图(self):
        allure.attach(self.driver.get_screenshot_as_png(),"截图",allure.attachment_type.PNG)

    def 断言文本(self,**kwargs):
        comparators={
            '>':lambda a,b:a>b,
            '<':lambda a,b:a<b,
            '==':lambda a,b:a==b,
            '>=':lambda a,b:a>=b,
            '<=':lambda a,b:a<=b,
            '!=':lambda a,b:a!=b,
            'in':lambda a,b:a in b,
        }
        message=kwargs.get("错误信息",None)
        compare_type=kwargs.get("断言类型","文本")
        operators=kwargs.get('比较符','==')

        if operators not in comparators:
            raise Exception(f'不支持的比较符，请输入正确的比较符{operators}')

        if compare_type=='数字':
            kwargs['期望结果']=float(kwargs['期望结果'])
        else:
            kwargs["期望结果"]=str(kwargs["预期结果"])

        if not comparators[operators](kwargs["实际结果"],kwargs["期望结果"]):
            if message:
                raise Exception(message)
            else:
                raise Exception(f"断言失败--{kwargs['实际结果']}{operators}{kwargs['实际结果']}")

    def 断言文本相等(self,**kwargs):
        kwargs.update({"比较符":"=="})
        # 断言
        self.断言文本(**kwargs)

    def 断言文本包含(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """
        kwargs.update({"比较符": "in"})
        self.断言文本(**kwargs)

    def 断言文本不相等(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """
        kwargs.update({"比较符": "!="})
        self.断言文本(**kwargs)

        # ---------------------断言数字方法--------------------------------

    def 断言数字相等(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """

        kwargs.update({"比较符": "==", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字不相等(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """
        kwargs.update({"比较符": "!=", "断言类型": "数字"})
        self.断言文本(**kwargs)

    ##3>5
    def 断言数字大于(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """
        kwargs.update({"比较符": ">", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字小于(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """
        kwargs.update({"比较符": "<", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字大于等于(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """
        kwargs.update({"比较符": ">=", "断言类型": "数字"})
        self.断言文本(**kwargs)

    def 断言数字小于等于(self, **kwargs):
        """
        调用 断言文本assert_text方法
        """
        kwargs.update({"比较符": "<=", "断言类型": "数字"})
        self.断言文本(**kwargs)
