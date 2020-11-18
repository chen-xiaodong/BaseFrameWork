"""

@FileName: method.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:21
@Descriptions:

"""
from tools.tool import *
from tools.tool import Yaml

# 加载config文件
config_file = Yaml(path="config/config.yaml")
config = config_file.load()
# 加载pages文件
pages_file = Yaml(path="config/pages.yaml")
# 获取配置项1
device_name = get_value_by_path(config, "appium_config.deviceName")
appium_config = get_value_by_path(config, "appium_config")
# 启动Adb
adb = Adb(device_name)
adb.connect()
# 启动Appium
app = Appium(desc=appium_config)
app.start_server()
# 启动driver
driver = app.start_driver()
driver.implicitly_wait(10)


def test_index(pages):
    username = get_value_by_path(pages, "index.username")
    username.click()
    password = get_value_by_path(pages, "index.password")
    password.send_keys()
    pages_obj = Pages(driver, pages)
    agree = pages_obj.get_value("pop.agree")
    agree.click()
    start_page = pages_obj.get_value("start")
    checkbox = get_value_by_path(start_page, "checkbox")
    checkbox.click()
    login = get_value_by_path(start_page, "login")
    login.click()


index_page: Dict = Pages(driver, pages_file.file).get_value("index")
test_index(index_page)
