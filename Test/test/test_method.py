"""

@FileName: test_method.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:21
@Descriptions: 

"""
import pytest

from basic_tool.adb import adb
from basic_tool.excel import excel_tools
from basic_tool.sql import sql_tools

#
# def test_adb():
#     adb_tool = adb().adb_start_server()
#     print(adb_tool)
#
#
# def test_db():
#     db = sql_tools("localhost", "root", "123456", "test", port=3306)
#     db.connect_mysql()
#     print(db.deal_sql("select * from user "))self.workbook.sheet_by_index(sheet)


# def test_excel():
#     excel = excel_tools("../../test3.xls")
#     excel.open_excel()
#     excel.change_sheet(2)
#     sheet = excel.get_row_values(2)
#     print(sheet)
from basic_tool.yaml import yaml_tools
from drivers.selenium import selenium_driver


def test_driver():
    # driver = selenium_driver("86.0.4240.22")
    # driver.get_webdriver_package()
    yaml = yaml_tools("../../drivers/driver_download.yaml")
    print(yaml.yaml_to_dict())


if __name__ == "__main__":
    test_driver()
