"""

@FileName: ddd.py
@Author: chenxiaodong
@CreatTime: 2020/11/10 10:36
@Descriptions: 

"""
import json
import os

# print(os.path.split(os.path.realpath(__file__))[0])
import requests

from tools.tool import Files, Zentao

# file = Files()
# file.zip_dir("reports", "report.zip")
# r = requests.Session()
#
# result = r.get("http://125.210.127.126:8080/zentao/api-getSessionID.json")
# results = result.json()
# print(results)
#
# if results.get("status") == "success":
#     data = json.loads(results.get("data"))
#     # print(type(json.loads(data)))
#     sessionID = data.get("sessionID")
#     sessionName = data.get("sessionName")
#     user = {
#         "account": "admin",
#         "password": "123456"
#     }
#
#     login_result = r.post("http://125.210.127.126:8080/zentao/user-login.json", data=user)
#     # print(login_result.json())
#     data = {
#         "product": "20",  # int   所属产品 * 必填
#         "openedBuild": "trunk",  # int | trunk   影响版本 * 必填
#         "branch": "2",  # int    分支 / 平台
#         "module": 0,  # int    所属模块
#         "project": "87",  # int   所属项目
#         "assignedTo": "op042052",  # string 指派给
#         "deadline": "",  # date 截止日期    日期格式：YY - mm - dd，如：2019 - 01 - 01
#         "type": "codeerror",
#         # string   Bug类型   取值范围： | codeerror | interface | config | install | security | performance | standard |
#         # automation | designchange | newfeature | designdefect | trackthings | codeimprovement | others
#         "os": "",
#         # string 操作系统 取值范围： | all | windows | win8 | win7 | vista | winxp | win2012 | win2008 | win2003 | win2000 |
#         # android | ios | wp8 | wp7 | symbian | linux | freebsd | osx | unix | others
#         "browser": "",
#         # string    浏览器 取值范围： | all | ie | ie11 | ie10 | ie9 | ie8 | ie7 | ie6 | chrome | firefox | firefox4 |
#         # firefox3 | firefox2 | opera | oprea11 | oprea10 | opera9 | safari | maxthon | uc | other
#         "color": "",  # string  颜色格式：  # RGB，如：#3da7f5
#         "severity": "1",  # int  严重程度    取值范围：1 | 2 | 3 | 4
#         "pri": "1",  # int   优先级 取值范围：0 | 1 | 2 | 3 | 4
#         "mailto": "",  # string 抄送给 填写帐号，多个账号用','分隔。
#         "keywords": "",  # string   关键词
#         "title": "324232",  # string  Bug标题 * 必填
#         "steps": "set bug link in here"  # string   重现步骤
#     }
#     creat_bug_result = r.post("http://125.210.127.126:8080/zentao/bug-create-20-0-87?"
#                               + sessionName + "=" + sessionID, data=data)
#     # print(json.dumps(creat_bug_result.json(), ensure_ascii=False))
#     print(creat_bug_result.content.decode("utf-8"))
data = {
    "product": "20",  # int   所属产品 * 必填
    "openedBuild": "trunk",  # int | trunk   影响版本 * 必填
    "branch": "2",  # int    分支 / 平台
    "module": 0,  # int    所属模块
    "project": "87",  # int   所属项目
    "assignedTo": "op042052",  # string 指派给
    "deadline": "",  # date 截止日期    日期格式：YY - mm - dd，如：2019 - 01 - 01
    "type": "codeerror",
    # string   Bug类型   取值范围： | codeerror | interface | config | install | security | performance | standard |
    # automation | designchange | newfeature | designdefect | trackthings | codeimprovement | others
    "os": "",
    # string 操作系统 取值范围： | all | windows | win8 | win7 | vista | winxp | win2012 | win2008 | win2003 | win2000 |
    # android | ios | wp8 | wp7 | symbian | linux | freebsd | osx | unix | others
    "browser": "",
    # string    浏览器 取值范围： | all | ie | ie11 | ie10 | ie9 | ie8 | ie7 | ie6 | chrome | firefox | firefox4 |
    # firefox3 | firefox2 | opera | oprea11 | oprea10 | opera9 | safari | maxthon | uc | other
    "color": "",  # string  颜色格式：  # RGB，如：#3da7f5
    "severity": "1",  # int  严重程度    取值范围：1 | 2 | 3 | 4
    "pri": "1",  # int   优先级 取值范围：0 | 1 | 2 | 3 | 4
    "mailto": "",  # string 抄送给 填写帐号，多个账号用','分隔。
    "keywords": "",  # string   关键词
    "title": "try it",  # string  Bug标题 * 必填
    "steps": "set bug link in here"  # string   重现步骤
}
Zentao("http://125.210.127.126:8080", "admin", "123456").create_bug(20, 0, 87, bug_data=data)
