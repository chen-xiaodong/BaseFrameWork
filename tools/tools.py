"""

@FileName: tools.py
@Author: chenxiaodong
@CreatTime: 2020/9/21 11:01
@Descriptions: 

"""
import smtplib
import subprocess
import sys
import types
import zipfile
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from functools import wraps
from json.decoder import JSONDecodeError
from queue import Queue
from time import sleep
import pymysql
import requests
import xlrd
import yaml
import logging
import logging.config
import allure
from benedict import benedict
from pathlib import Path
from selenium import webdriver
from threading import Thread
from typing import Optional, Dict, Any, Union, Type
from appium import webdriver as app_webdriver
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver as AppWebDriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from selenium.webdriver.remote.webelement import WebElement

_LOGLEVEL: int
_LOG_PATH: str
_LoggerConfig: Dict
logger: logging.Logger


def retry(retry_time: int = 3):
    """
    方法重试装饰器。

    用于重新执行某方法retry_time次

    :Params retry_time: 重试次数
    :Returns:
    """

    def adb_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for time in range(retry_time):
                logger.info("重试第" + str(time + 1) + "次")
                func(*args, **kwargs)
                sleep(1)

        return wrapper

    return adb_wrapper


def device_check(func):
    """
    检查是否有adb设备连接的装饰器。

    若存在连接，则继续执行；不存在连接，则中断执行

    :Params func: 方法
    :Returns:
    """

    def wrapper(*args, **kwargs):
        adb = Adb()
        if adb.devices() == "":
            # adb.connect()
            print("无设备连接")
            pass
        else:
            func(*args, **kwargs)

    return wrapper


def set_log(level: int = 10, path: str = "test.log", logger_config: Dict = None):
    """
    设置log日志文件的存储路径
    设置log记录级别

    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    """
    global _LOG_PATH, _LOGLEVEL, _LoggerConfig
    _LOG_PATH = path
    _LOGLEVEL = level
    _LoggerConfig = logger_config


def log():
    """
    log装饰器

    用于装饰所需要进行log处理的方法

    :Params
    :Returns
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            # logging.basicConfig(filename=_LOG_PATH, level=_LOGLEVEL, filemode="w",
            #                     format='%(levelname)s %(asctime)s %(message)s',
            #                     datefmt='%Y/%m/%d %I:%M:%S '
            #                     )
            # global logger
            # logger = logging.getLogger(__name__)
            # # print("name")
            # global _Logger_Config
            args1 = "  参数: " + str(args) if args else ""
            args2 = "  固定位置参数: " + str(kwargs) if kwargs else ""
            logging.config.dictConfig(_LoggerConfig)
            global logger
            logger = logging.getLogger(__name__)
            logger.info(func.__name__ + args1 + args2)
            result = func(*args, **kwargs)
            logger.info("result:  " + str(result))
            return result

        return inner

    return func_wrapper


def singleton(cls):
    """
    单例模式装饰器


    :param cls:
    :returns: Any
    """
    _instance = {}

    def inner(*args, **kw):
        key = str(args) + str(kw)
        if str(cls) + key not in _instance.keys():
            _instance[str(cls) + key] = cls(*args, **kw)
        return _instance[str(cls) + key]

    return inner


class Adb:
    """
    Adb类

    包含adb相关操作

    :param device: 设备名称


    Usage::
        >>> adb =Adb(device = "127.0.0.1:6556")


    """

    # @log()
    def __init__(self, device: str = ""):
        self._device = device

    def adb_kill_server(self):
        """关闭 adb 服务"""
        self.run("adb kill-server")

    def adb_start_server(self):
        """启动adb 服务"""
        self.run("adb start-server")

    def adb_shell(self, args):
        """执行adb shell 命令
        :param args: shell命令参数
        """
        self.run("adb shell " + args)

    @log()
    @retry()
    def connect(self):
        """adb连接设备
        连接失败默认重试连接三次，连接失败后结束运行
        """
        result = self.run("adb connect " + self._device)
        if "failed" in result:
            logger.error("设备连接失败！ Error Message: " + str(result))

    def devices(self):
        """
        输出adb当前连接的设备

        :param:
        :return: devices list


        adb 会针对每个设备输出以下状态信息：

        序列号：由 adb 创建的字符串，用于通过端口号唯一标识设备。 下面是一个序列号示例：emulator-5554
        状态：设备的连接状态可以是以下几项之一：
            offline：设备未连接到 adb 或没有响应。
            device：设备现已连接到 adb 服务器。请注意，此状态并不表示 Android 系统已完全启动并可正常运行，因为在设备连接到 adb 时系统仍在启动。不过，在启动后，这将是设备的正常运行状态。
            no device：未连接任何设备。
        说明：如果您包含 -l 选项，devices 命令会告知您设备是什么。当您连接了多个设备时，此信息很有用，可帮助您将它们区分开来。

        """
        msg = self.run("adb devices")
        device = msg.splitlines()[1].split('\t')[0]
        return device

    @device_check
    def adb_install(self, args="-a", package: str = ""):
        """
        adb安装apk应用

        :param args: 安装参数，默认为"-a"
        :param package: apk名称

        """
        self.run("adb install " + args + package)

    @device_check
    def adb_uninstall(self, args="-a", package: str = ""):
        """
        adb卸载apk应用

        :param args: 卸载参数，默认为"-a"
        :param package: apk名称，默认为空

        """
        self.run("adb uninstall " + args + package)

    @device_check
    def adb_start(self, activity: str = ""):
        """

        :param activity:应用activity名称
        :return:
        """
        self.run("adb  shell am start -n " + activity)

    @device_check
    @log()
    def up(self):
        """adb模拟键盘上键"""
        self.run("adb shell input keyevent 19")

    @log()
    @device_check
    def down(self):
        """adb模拟键盘下键"""
        self.run("adb shell input keyevent 20")

    @log()
    @device_check
    def right(self):
        """adb模拟键盘右键"""
        self.run("adb shell input keyevent 22")

    @log()
    @device_check
    def left(self):
        """adb模拟键盘左键"""
        self.run("adb shell input keyevent 21")

    @log()
    @device_check
    def ok(self):
        """adb模拟确定键"""
        self.run("adb shell input keyevent 66")

    @log()
    @device_check
    def back(self):
        """adb模拟手机返回键"""
        self.run("adb shell input keyevent 4")

    @log()
    @device_check
    def input_nums(self, nums: str):
        """
        输入数字

        :param nums: 数字字符串
        :return:
        """
        for num in nums:
            num = str(int(num) + 7)
            self.run("adb shell input keyevent " + num)

    @staticmethod
    def run(args):
        """
        执行shell命令

        默认为shell模式

        :param args: 执行shell的参数
        :return str: 执行结果
        """
        p = subprocess.run(args=args, shell=True, stdout=subprocess.PIPE)
        return p.stdout.decode("utf-8")


class Excel:
    """
    Excel类，用于操作excel表格获取数据

    :param path: excel文件路径
    :param workbook: excel工作簿，默认为None
    :param sheet_index: sheet默认索引值
    :param sheet: sheet对象，默认为None

    Usage::
        >>> excel = Excel(path="test.xls")
        >>> excel.open()
        >>> value = excel.cell_value(5,6)


    """

    def __init__(self, path="", workbook=None, sheet_index=0, sheet=None):
        self.path = path
        self.workbook = workbook
        self.sheet_index = sheet_index
        self.sheet = sheet

    def open(self):
        """打开一个excel表，对象需要先执行此方法后再调用其他方法"""
        self.workbook = xlrd.open_workbook(self.path)
        self.sheet = self.workbook.sheet_by_index(self.sheet_index)

    def change_sheet(self, sheet_index):
        """
        切换sheet

        :param sheet_index:sheet的索引值
        """
        self.sheet = self.workbook.sheet_by_index(sheet_index - 1)

    def cell_value(self, x_point: int = 1, y_point: int = 1) -> str:
        """
        获取单元格的返回值

        :param x_point: 行数，默认值为第一行
        :param y_point: 列数，默认值为第一列
        :return str    单元格所在的值
        """
        return self.sheet.cell_value(x_point - 1, y_point - 1)

    def row_values(self, x_point: int = 1) -> list:
        """
        获取某行的所有值

        :param x_point: 行数，默认为第一行
        :return list: 返回值的列表
        """
        if isinstance(x_point, int):
            return self.sheet.row_values(x_point - 1)

    def col_values(self, y_point: int = 1) -> list:
        """
        获取一列的所有值

        :param y_point: 列数，默认为第一列
        :return list: 返回值列表
        """
        if isinstance(y_point, int):
            return self.sheet.col_values(y_point - 1)


class MyQueue(Queue):
    """
    MyQueue队列类，用于队列的操作


    """

    def __init__(self):
        super().__init__()

    def empty(self) -> bool:
        """
        判断队列是否为空队列

        :returns bool 返回队列是否为空
        """
        return super().empty()

    def full(self) -> bool:
        """
        判断队列是否已经达到最大值

        :returns bool 返回队列是否已满
        """
        return super().full()

    def put(self, item, block: bool = ..., timeout: Optional[float] = ...) -> None:
        super().put(item, block, timeout)

    def join(self) -> None:
        super().join()

    def qsize(self) -> int:
        return super().qsize()

    def task_done(self) -> None:
        super().task_done()


class MyThread(Thread):
    """
    线程类。继承了Thread类

    """

    def __init__(self, func):
        super().__init__()
        self.target = func

    def run(self) -> None:
        super().run()


class Files:
    def __init__(self):
        pass

    def download_file(self, source_url="", path=""):
        if self.check_file_is_exist(path):
            return path
        else:
            url = source_url
            req = requests.get(url)
            with open(path, "wb") as file:
                file.write(req.content)

    def check_file_is_exist(self, file_name):
        if file_name in self.get_list_dir():
            return True
        else:
            return False

    @staticmethod
    def get_current_file_path():
        return str(Path().resolve())

    @staticmethod
    def get_list_dir():
        return [str(x) for x in Path().iterdir()]

    @staticmethod
    def mkdir(filepath):
        if Path(filepath).exists():
            return
        else:
            Path(filepath).mkdir()


class SqlClass:
    """
    数据库类，对Mysql数据库有效

    :param host: mysql的host地址
    :param username: mysql用户名
    :param password: mysql密码
    :param dbName: 数据库名称
    :param db: 数据库连接对象
    :param port: 数据库端口
    """

    def __init__(self, host, username, password, dbName, db=None, port=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbName = dbName
        self.db = db

    def connect_mysql(self):
        """
        连接mysql数据库
        """
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.username,
                                  password=self.password, db=self.dbName)

    def deal_sql(self, sql_str):
        """
        处理SQL语句

        :param sql_str: sql操作语句
        :return:
        """
        cursor = self.db.cursor()
        cursor.excute(sql_str)
        return cursor


@singleton
class Yaml:
    """
    处理yaml文件类

    :param path: yaml文件路径
    :param file: yaml文件转换后的DICT对象


    """

    def __init__(self, path: str = "", file: Dict = None) -> None:
        self.path = path
        self.file = file

    def load(self):
        """
        用于加载yaml文件，获取yaml文件中的值时需要先调用此方法，只需调用一次。
        路径错误则结束运行，并记录在日志

        :raise FileNotFoundError

        """
        try:
            with open(self.path, "rb") as f:
                self.file = yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error("文件路径错误，请检查! Error Message：" + str(e))

    def get_config_by_path(self, config_path="") -> Any:
        """
        通过传入配置项的路径获取该项值

        路径为str类型，如： config.app.version


        :param config_path: 配置项路径
        :return: Any
        """

        try:
            dic = benedict(self.file)
            return dic[config_path]
        except TypeError as e:
            logger.error("文件不存在或无法找到对应的键值！Error Message：" + str(e) +
                         "\n  参数值：" + config_path)


@singleton
@log()
class Appium:
    """
    Appium类，集成了appium的操作

    :param address: appium server地址
    :param port: appium server端口
    :param desc: appium server配置

    """

    def __init__(self, address: str = "localhost", port: int = 4723,
                 desc: Optional[Dict] = None):
        self.address = address
        self.port = port
        self.url = "http://" + address + ":" + str(port) + "/wd/hub"
        self.desc = desc
        self.driver = None
        self.service = None

    def start_server(self):
        """启动appium server"""
        self.service = AppiumService()
        if self.service.is_listening:
            logger.info("appium server is started")
        else:
            self.service.start()

    def start_driver(self):
        """启动appium driver"""
        if self.service.is_listening:
            try:
                self.driver = app_webdriver.Remote(self.url, self.desc)
                return self.driver
            except WebDriverException as e:
                logger.error("driver启动失败，请重试")
                return None
        else:
            self.start_server()


@singleton
class Selenium(object):
    """
    Selenium类，用于selenium相关操作

    :param version: 浏览器版本
    :param platform: 平台
    :param config_dir: 配置文件目录
    :param yaml_file_path: 配置文件路径
    :param driver_zip: 压缩文件名称
    """

    def __init__(self, version: str = "", platform: str = "", config_dir: str = "",
                 yaml_file_path: str = "", driver_zip: str = "",
                 driver=None):
        self._version = version
        self._platform = platform
        self._config_dir = config_dir
        self._config_file = yaml_file_path
        self._yaml_file = None
        self._driver = driver
        self._driver_zip = driver_zip
        if self._platform == "windows":
            self._driver_path = self._config_dir + "/chromedriver.exe"
        else:
            self._driver_path = self._config_dir + "/chromedriver"

    def get_webdriver_package(self):
        file_tool = Files()
        if file_tool.check_file_is_exist(self._config_dir):
            if file_tool.check_file_is_exist(self._driver_path):
                return self._driver_path
            else:
                self._yaml_file = Yaml(self._config_dir + self._config_file)
                url = self._yaml_file.get_config_by_path(
                    "download_url.base_url") + self._version + self._yaml_file.get_config_by_name(self._platform)
                f = requests.get(url, stream=True)
                with open(self._driver_zip, "wb") as file:
                    file.write(f.content)
                z = zipfile.ZipFile(self._driver_zip, 'r')
        else:
            file_tool.mkdir(self._config_dir)

    def start_driver(self):
        """启动selenium driver"""
        self._driver = webdriver.Chrome(executable_path=self.get_webdriver_package())
        self._driver.get(self._yaml_file.get_config_by_name("selenium_url"))
        return self._driver


def dell_keyevent(operations):
    """处理adb 键值响应"""
    adb = Adb()
    opts = {
        "up": adb.up(),
        "down": adb.down(),
        "ok": adb.ok(),
        "left": adb.left(),
        "right": adb.right(),
    }
    for operation in operations:
        operation: str
        if "input" in operation:
            value = operation.split(' ')[1]
            adb.input_nums(value)
        else:
            opts.get(operation)
        sleep(1)


@log()
class CaseLoader:
    """
    CaseLoader类，用例加载类

    :param file: yaml文件
    :param case_list:执行用例列表
    :param name:配置文件"name"的名称
    :param actions:配置文件"acitons"的名称
    :param refer:配置文件"refer"的名称
    :param operation:配置文件"operation"的名称
    :param locate:配置文件"locate"的名称
    :param element:配置文件"element"的名称
    :param value:配置文件"value"的名称
    :param validate:配置文件"validate"的名称
    :param driver:appium driver对象
    """

    def __init__(self, file: Yaml = None,
                 case_list: list = None,
                 name: str = "name", actions: str = "actions",
                 refer: str = "refer", operation: str = "operation",
                 locate: str = "locate", element: str = "element", value: str = "value",
                 validate: str = "",
                 driver: Union[Type[SeleniumWebDriver], Type[AppWebDriver]] = None
                 ):

        self.validate = validate
        self.file = file
        self.case_list = case_list
        self.value = value
        self.actions = actions
        self.name = name
        self.actions = actions
        self.refer = refer
        self.operation = operation
        self.locate = locate
        self.element = element
        self.driver = driver

    def start(self) -> None:

        pass

    def get_case(self, case_name) -> Dict:
        """
        获取用例，返回dict

        :param case_name:用例名称
        """
        if self.file.get_config_by_path(case_name):
            return self.file.get_config_by_path(case_name)

    def get_refer(self, case_name) -> str:
        """
        获取refer

        :param case_name:
        """
        if self.file.get_config_by_path(case_name + ".refer"):
            return self.file.get_config_by_path(case_name + ".refer")

    def check_refer(self, case: Dict = None) -> bool:
        """校验是否存在refer"""
        return True if case.get(self.refer) else False

    def get_element(self, method: str = "", element: str = "") -> Any:
        """获取element"""
        try:
            if method == "id":
                # print(element)
                return self.driver.find_element_by_id(element)
            elif method == "name":
                return self.driver.find_element_by_name(element)
            elif method == "xpath":
                return self.driver.find_element_by_xpath(element)
            elif method == "class":
                return self.driver.find_element_by_class_name(element)
        except NoSuchElementException as e:
            print("没有找到这个元素，请检查元素定位信息")

    @staticmethod
    def opt(element: WebElement, operation: str = "", value: str = "") -> None:
        """对element进行操作"""
        try:
            if operation == "click":
                element.click()
            elif operation == "send_keys":
                element.send_keys(value)
            elif operation == "text":
                return element.text

        except AttributeError as e:
            logger.debug("元素属性错误，请检查后再试! Error Message:" + str(e))
        except NoSuchElementException as e:
            logger.error("无法找到该元素，请重试！ Error Message:" + str(e))

    def dell_action(self, actions: Dict = None):
        """处理action"""
        for case, actions in actions.items():
            print(actions)
            locate = actions.get(self.locate)
            element = actions.get(self.element)
            operation = actions.get(self.operation)
            value = actions.get(self.value)
            validate = actions.get(self.validate)
            element = self.get_element(locate, element)
            if locate is None and element is None:
                dell_keyevent(operation)
            else:
                self.opt(element, operation, value)
            self.dell_validate(validate)

    def dell_refer(self, refer) -> Any:
        """处理refer"""
        case = self.get_case(refer)
        self.dell_case(case)

    def dell_case(self, case):
        """处理case"""
        refer = case.get(self.refer)
        actions = case.get(self.actions)
        validate = case.get(self.validate)
        name = case.get(self.name)

        if refer is None:
            pass
        else:
            self.dell_refer(refer)
        self.dell_action(actions)
        if validate is None:
            pass
        else:
            self.dell_validate(validate)

    def load(self, time: int = 3) -> None:
        """加载用例"""
        # 判断是否开启driver
        print(self.driver)
        if self.driver is None:
            logger.error("无法获取driver，请先启动driver")
            sys.exc_info()
            sys.exit(0)
            # raise BaseException("无法获取driver，请先启动driver")
        # 设置全局等待时间，默认3s
        self.driver.implicitly_wait(time_to_wait=time)
        # 新建队列
        queue = MyQueue()
        # 将case名放入队列
        for item in self.case_list:
            case = self.get_case(item)
            queue.put(case)
        while True:
            if queue.empty():
                break
            case = queue.get()
            self.dell_case(case)

    def dell_validate(self, validates):
        """处理校验"""
        if validates:
            url = validates.get("url")
            activity = validates.get("activity")
            texts = validates.get("text")
            try:
                if url:
                    current_url = self.driver.current_url
                    except_url = url.get("except")
                    assert current_url == except_url
                if activity:
                    current_activity = self.driver.current_activity
                    except_activity = activity.get("except")
                    assert current_activity == except_activity
                if texts:
                    locate: str = texts.get(self.locate)
                    element: str = texts.get(self.element)
                    except_text: str = texts.get("except")
                    elements: WebElement = self.get_element(locate, element)
                    assert elements.text == except_text
            except AssertionError as error:
                logger.error("断言失败" + str(error))
            except AttributeError as error2:
                logger.error("无法获取到键值" + str(error2))
        else:
            pass


class Request:
    """
    Request类，用于处理请求

    :param url: 请求url
    :param method: 请求方式
    :param data: 请求数据
    """

    def __init__(self, url: str, method: str = "get", data: Any = None):
        self.url = url
        self.session = requests.Session()
        self.method = method
        self.data = data

    def req(self):
        result = None
        if self.method == "get":
            result = self.session.get(self.url)
        elif self.method == "post":
            result = self.session.post(self.url, data=self.data)
        try:
            final = result.json()
            return final
        except UnicodeDecodeError as error:
            pass
        except JSONDecodeError as error2:
            pass


class Mail:
    """
    Mail类，用于发送邮件

    :param username: 邮箱用户名
    :param password: 邮箱密码
    :param address: 收件人地址
    """

    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.address = address
        self.message = None
        self.server = None

    def send(self, header_msg: str = "", to_msg: str = "",
             subject: str = "", server_address: str = "", port: int = 465, files: list = None):
        # self.message = MIMEMultipart()

        self.message = MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8')
        self.message['FROM'] = formataddr([header_msg, self.username])
        self.message['To'] = formataddr([to_msg, self.address])
        self.message['subject'] = subject
        self.login(server_address, port)
        if files:
            self.set_files(files)
        else:
            pass
        self.server.sendmail(self.username, [self.address], self.message.as_string())

    def login(self, address, port):
        self.server = smtplib.SMTP_SSL(address, port)
        self.server.login(self.username, self.password)

    def set_files(self, files: list = None):
        for file in files:
            att1 = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; '
            self.message.attach(att1)


class Report:
    def __init__(self, level):
        self.level = level

    def allure_report(self):
        pass

    def html_report(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


class Zentao:
    def __init__(self):
        pass


class errorHandler:
    def __init__(self):
        pass
