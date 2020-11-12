"""

@FileName: test_add.py
@Author: chenxiaodong
@CreatTime: 2020/10/27 09:38
@Descriptions: 

"""
# !/usr/bin/env python
# coding=utf-8
import allure
import pytest
import os


@allure.feature("测试加法")
def test1():
    assert 2 == 2


@allure.story("测试减法")
def test2():
    assert 3 == 4


@allure.step("步骤1")
def test3():
    print("buzhouhhhhh")


@allure.step("步骤2")
def test4():
    print("步骤2开始执行")
    allure.attach("这是附加内容")
    # with open("Test/test/test.jpg", "r") as f:
    allure.attach.file("Test/test/test.jpg", "test.jpg", attachment_type=allure.attachment_type.JPG)


if __name__ == "__main__":
    # 执行pytest单元测试，生成 Allure 报告需要的数据存在 /temp 目录
    pytest.main(['--alluredir', './temp'])
    # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
    os.system('allure generate ./temp -o ./report --clean')
# import sys
# print(sys.argv[0]) # will print the file name
# # allure_package(sys.argv[0].rsplit('.', 1)[0])
# print((sys.argv[0].rsplit('.',1)[0]).replace('/','.'))
# import os
# print(os.getcwd())#获得当前工作目录
# print(os.path.abspath('.'))#获得当前工作目录
# print(os.path.abspath('../'))#获得当前工作目录的父目录
# print(os.path.abspath(os.curdir))
