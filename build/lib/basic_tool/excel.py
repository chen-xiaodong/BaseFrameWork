"""

@FileName: excel.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 10:56
@Descriptions: 

"""
import xlrd


class excel_tools:
    def __init__(self, path, workbook=None):
        self.path = path
        self.workbook = workbook

    def open_excel(self):
        self.workbook = xlrd.open_workbook(self.path)

    def get_sheet(self, sheet_index):
        """

        :param sheet_index:sheet的索引值，默认值为1
        :return:
        """
        return self.workbook.sheet_by_index(sheet_index)

    def get_cell_value(self, sheet_index=1, x_point=1, y_point=1) -> str:
        """

        :param sheet_index: sheet的索引值，默认值为1
        :param x_point: 行数
        :param y_point: 列数
        :return: str    单元格所在的值
        """
        return self.get_sheet(sheet_index - 1).cell_value(x_point - 1, y_point - 1)
