"""

@FileName: test1.py
@Author: chenxiaodong
@CreatTime: 2020/11/17 下午3:09
@Descriptions: 

""""""

@FileName: method.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:21
@Descriptions:

"""
from tools.tool import *

# 加载config文件
config_file = Yaml(path="config/config.yaml")
config = config_file.load()
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
# 加载用例
case_list = ["case2"]
cases = CaseLoader(config, case_list, driver=driver)
# 运行
cases.load(10)

