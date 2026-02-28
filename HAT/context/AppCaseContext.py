from HAT.core.globalContext import g_context
from appium import webdriver
from HAT.keywords.app_keywords import Keywords
import allure
from base64 import b64decode
from appium.webdriver.extensions.android.nativekey import AndroidKey
import atexit

_global_driver_obj=None
def cleanup_context():
    if _global_driver_obj is not None:
        try:
            _global_driver_obj.press_keycode(AndroidKey.HOME)
            _global_driver_obj.quit()
        except Exception as e:
            print("设备关闭失败")

atexit.register(cleanup_context)


class AppCaseContext:
    def __init__(self):
        self.keywords=None
        self.driver=None

    def initDriver(self):
        _appiumServer_config = g_context().get_dict("设备列表")["appiumServer"]  # appium服务信息
        _desiredCapabilities_config = g_context().get_dict("设备列表")["desiredCapabilities"]

        remote_host = _appiumServer_config['remoteHost']  # 127.0.0.1
        remote_port = _appiumServer_config['remotePort']  # 4723
        remote_path = _appiumServer_config.get('remotePath', '')

        appiumServer=f"http://{remote_host}:{remote_port}{remote_path}"
        driver=webdriver.Remote(appiumServer,_desiredCapabilities_config)

        return driver

    def init_keywords(self):
        session_reuse=g_context().get_dict("session_reuse")
        if session_reuse is not None and session_reuse==True:
            global _global_driver_obj  # 全局变量 针对这个模块的全局变量
            if _global_driver_obj is None:  # 第一次运行
                _global_driver_obj = self.initDriver()  # 启动设备 保存在全局变量中
            self.driver = _global_driver_obj
        else:
            self.driver=self.initDriver()
        self.keyworads=Keywords(self.driver)
        return self.keywords

    def start(self):
        self.driver.start_recording_screen()

    def release(self):
        # 设备启动了
        if self.driver is not None:
            try:
                # 关闭录屏
                screen_recording = self.driver.stop_recording_screen()
                # 录屏记录到allure报告中
                allure.attach(
                    b64decode(screen_recording),
                    name="录屏回放",
                    attachment_type=allure.attachment_type.MP4
                )
            except Exception as e:
                print("没有录屏,录屏失败处理")
            finally:
                # 没有复用
                if not g_context().get_dict("session_reuse"):
                    try:
                        # 按下Home键返回桌面
                        self.driver.press_keycode(AndroidKey.HOME)
                    except Exception as e:
                        print("没有返回桌面")
                    finally:
                        self.driver.quit()