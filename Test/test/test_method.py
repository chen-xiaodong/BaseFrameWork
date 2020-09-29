#! /usr/bin/env python3
"""

@FileName: test_method.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:21
@Descriptions: 

"""
from tools.tools import *

config_file = Yaml(path="config/config.yaml")
file = config_file.load()
appium_config = config_file.get_config_by_path("appium_config")
devices = config_file.get_config_by_path("device_ip2")
print(devices)
adb = Adb(devices)
adb.connect()
app = Appium(desc=appium_config)
# app.start_server()
driver = app.start_driver()
case_list = ["case2"]
cases = CaseLoader(config_file, case_list, driver=driver)
cases.load(10)
