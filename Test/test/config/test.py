"""

@FileName: test.py
@Author: chenxiaodong
@CreatTime: 2020/10/30 11:20
@Descriptions: 

"""
import numpy as np
import pandas as pd

with pd.ExcelFile("../resources/test3.xls") as xls:
    df1 = pd.read_excel(xls, "Sheet1")
    df2 = pd.read_excel(xls, "Sheet2")
    print(df1["phone"])
    print(type(df1["phone"]))
