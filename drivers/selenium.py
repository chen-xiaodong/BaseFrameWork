"""

@FileName: selenium.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:01
@Descriptions: 

"""
import pathlib

import requests

from selenium import webdriver

from basic_tool.yaml import yaml_tools
from schedule.wrappers import singleton


@singleton
class selenium_driver:

    def __init__(self, version="", platform="", path="", driver=None):
        self._version = version
        self._platform = platform
        self._config_file = yaml_tools(path)
        self._driver = driver

    def get_webdriver_package(self, download_file_path=""):
        if pathlib.Path(download_file_path).exists():
            return download_file_path
        else:
            url = self._config_file.get_config_by_name("base_url") + \
                  self._version + self._config_file.get_config_by_name("macos")
            f = requests.get(url)
            with open(download_file_path, "wb") as file:
                file.write(f.content)
            return download_file_path

    def start_driver(self, file_path=""):
        self._driver = webdriver.Chrome(self.get_webdriver_package(file_path))
        self._driver.get(self._config_file.get_config_by_name("selenium_url"))
        return self._driver


