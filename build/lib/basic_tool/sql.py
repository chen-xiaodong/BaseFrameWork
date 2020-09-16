"""

@FileName: sql.py
@Author: chenxiaodong
@CreatTime: 2020/9/15 11:07
@Descriptions: 

"""
import pymysql


class sql_tools:
    def __init__(self, host,  username, password, dbName, db=None, port=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbName = dbName
        self.db = db

    def connect_mysql(self):
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.username,
                                  password=self.password, db=self.dbName)

    def deal_sql(self, sql):
        cursor = self.db.cursor()
        cursor.excute(sql)
        return cursor
