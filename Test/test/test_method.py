#! /usr/bin/env python3
"""

@FileName: test_method.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:21
@Descriptions: 

"""

from tools.tools import *

# 基础测试流程
# 设置记录log记录级别和路径
set_log(path="config/xxx.log")
# 配置文件加载
config_file = Yaml(path="config/config.yaml")
config_file.load()
opts = config_file.get_config_by_path("before_case2.actions.action1.operations")
# adb = Adb()
# adb.devices()
# dell_keyevent(opts)
# appium_config = config_file.get_config_by_path("appium_config")
# devices = config_file.get_config_by_path("device_ip2")
# adb = Adb(devices)
# print(adb)
# adb.connect()
# app = Appium(desc=appium_config)
# # app.start_server()
# driver = app.start_driver()
# case_list = ["case2"]
# cases = CaseLoader(config_file, case_list, driver=driver)
# cases.load(10)
# log测试
# logtest(b=1)
# opts = ["up","up","left","right"]
# dell_keyevent(opts)
# adb = Adb()
# adb.input_nums("1345678")
