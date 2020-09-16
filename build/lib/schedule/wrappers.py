"""

@FileName: wrappers.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 13:49
@Descriptions: 

"""


def adb_wrapper(func):
    def wrapper(*args, **kwargs):
        u = func()
        return u
    return wrapper()

