# """
#
# @FileName: test.py
# @Author: chenxiaodong
# @CreatTime: 2020/9/30 11:06
# @Descriptions:
#
# """
# import requests
# import json
#
# url1 = "https://www.maxluck.top/api/hdzbstb/museum/queryMyMuseum"
# url2 = "sssss.com"
#
# data = {
#     "studentId": "29571",
# }
# data2 = {"studentId": "29571"}
# # 调用查询接口
# r = requests.post(url1, data)
# # 将返回值转成Python内置类型dict
# dict1 = r.json()
# # 赋值给变量
# signStatus = dict1.get("data").get("isSignIn")
# # 判断是否签到
# if signStatus:
#
#     # 未签到， 调用签到接口
#     # r2 = requests.post(url2, data2)
#     # dict2 = r2.json()
#     # 获取返回值，
#     pass
# else:
#     # 签到后，查询签到日历
#     # 获取今日是否签到
#     # 判断: 如果日历显示今日未签到，接口有问题
#     # 如果日历显示今日已签到，接口正常
#     pass
with open("requirements.txt", "r") as fh:
    long_description = fh.readlines()
    print(long_description)
