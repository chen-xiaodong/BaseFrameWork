"""

@FileName: ddd.py
@Author: chenxiaodong
@CreatTime: 2020/11/10 10:36
@Descriptions: 

"""
import os

# print(os.path.split(os.path.realpath(__file__))[0])
from tools.tool import Files


# file = Files()
# file.zip_dir("reports", "report.zip")
def add():
    print("1")
    yield 2
    print("2")


def b():
    print("3")
    add()
    print("4")


if __name__ == '__main__':
    b()
