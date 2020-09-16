"""

@FileName: adb.py
@Author: chenxiaodong
@CreatTime: 2020/9/14 16:23
@Descriptions: 

"""
import subprocess


class adb:
    def __init__(self):
        """
        :param:
        :return:

        """
        pass

    def adb_kill_server(self):
        """
        :param:
        :return:

        """
        self.run("adb kill-server")

    def adb_start_server(self):
        """
        :param:
        :return:

        """
        self.run("adb start-server")

    def adb_shell(self, args):
        """
        :param:
        :return:

        """
        self.run("adb shell " + args)

    def adb_connect(self, device: str):
        """
        :param:
        :return:

        """
        self.run("adb connect " + device)

    def adb_devices(self):
        """
        :param:
        :return:

        """
        pass

    def adb_install(self, args="-a", package=None):
        """
        :param: 
        :return: 
        
        """
        self.run("adb install " + args + package)

    def adb_uninstall(self, args="-a", package=None):
        """
        :param:
        :return:

        """
        self.run("adb uninstall " + args + package)

    @staticmethod
    def run(args):
        p = subprocess.run(args=args, shell=True, stdout=subprocess.PIPE)
        return p
