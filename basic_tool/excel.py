"""

@FileName: excel.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 10:56
@Descriptions: 

"""
import xlrd


class excel_tools:
    def __init__(self, path="", workbook=None, sheet_index=0, sheet=None):
        self.path = path
        self.workbook = workbook
        self.sheet_index = sheet_index
        self.sheet = sheet

    def open_excel(self):
        """
        打开一个excel表
        :return:
        """
        self.workbook = xlrd.open_workbook(self.path)
        self.sheet = self.workbook.sheet_by_index(self.sheet_index)

    def change_sheet(self, sheet_index):
        """
        切换sheet
        :param sheet_index:sheet的索引值
        :return:
        """
        self.sheet = self.workbook.sheet_by_index(sheet_index-1)

    def get_cell_value(self, x_point=1, y_point=1) -> str:
        """
        获取单元格的返回值
        :param x_point: 行数
        :param y_point: 列数
        :return: str    单元格所在的值
        """
        return self.sheet.cell_value(x_point-1, y_point-1)

    def get_row_values(self, x_point=1) -> list:
        """
        获取一行的所有值，返回一个值的列表
        :param x_point:
        :return: list
        """
        return self.sheet.row_values(x_point-1)

    def get_col_values(self, y_point=1) -> list:
        """
        获取一列的所有值，返回一个值的列表
        :param y_point:
        :return: list
        """
        return self.sheet.col_values(y_point-1)
