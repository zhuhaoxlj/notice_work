# 目前只适配了 Mac OS
# 测试平台：Mac OS 14.0
# Python 版本：3.11.4
# TODO 我正在完成任务的时候不要弹出
# TODO 加入判断当前cookies是否生效，如果失效了提醒登录获取cookies
# TODO 如果这次的数据和上次的不一样才提醒，午休时间不提醒，延后提醒
import threading
from collections import Counter
import tkinter as tk
from pynput import keyboard
from bs4 import BeautifulSoup
from pync import Notifier
import os
from dotenv import load_dotenv
import rumps
import json
import time
import rumps
from urllib.parse import urljoin
import browser_cookie3
import requests
from dotenv import load_dotenv
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt  # 导入 Qt 模块

cookies = ""
data = dict()
file_name = "work_data.json"
is_first_init = True
# 加载.env文件
load_dotenv()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录窗口")
        self.setGeometry(100, 100, 200, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建用户名标签和输入框
        self.username_label = QLabel("用户名:")
        self.username_entry = QLineEdit()
        # 设置输入法为数字和英文
        self.username_entry.setInputMethodHints(
            Qt.ImhDigitsOnly | Qt.ImhPreferLatin)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)

        # 创建密码标签和输入框
        self.password_label = QLabel("密码:")
        self.password_entry = QLineEdit()
        # 设置输入法为数字和英文
        self.password_entry.setInputMethodHints(
            Qt.ImhDigitsOnly | Qt.ImhPreferLatin)
        self.password_entry.setEchoMode(QLineEdit.Password)  # 使密码框显示星号
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)

        # 创建登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.on_login_button_click)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        # 设置窗口顶置
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        # 将密码输入框的回车键绑定到登录按钮的点击事件
        self.password_entry.returnPressed.connect(self.login_button.click)

    def on_login_button_click(self):
        # 获取用户名和密码输入框的文本
        username = self.username_entry.text()
        password = self.password_entry.text()
        login_get_cookie(username, password)
        # 打印用户名和密码
        # print("用户名:", username)
        # print("密码:", password)


def main():
    # 检查是否已经存在 QApplication 实例
    existing_instance = QApplication.instance()
    if existing_instance:
        # 销毁现有的 QApplication 实例
        existing_instance.quit()

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    window.activateWindow()
    sys.exit(app.exec())


def login_get_cookie(username, password):
    url = 'http://wss.gkoudai.com/index.php?m=user&f=login'
    global cookies
    cookies = browser_cookie3.chrome(domain_name='wss.gkoudai.com')
    # 创建一个session,作用会自动保存cookie
    session = requests.session()
    data = {
        'account': username,
        'password': password,
        'keepLogin': 1
    }
    # 使用session发起post请求来获取登录后的cookie,cookie已经存在session中
    response = session.post(url=url, data=data, cookies=cookies)
    cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
    return cookies_dict


def string_to_dict(cookie_string):
    cookie_dict = {}
    pairs = cookie_string.split("; ")

    for pair in pairs:
        key, value = pair.split("=")
        cookie_dict[key] = value
    return cookie_dict


def write_response_to_html(response):
    # 检查响应状态码，确保请求成功
    if response.status_code == 200:
        # 定义文件名
        file_name = 'response.html'

        # 将响应内容写入文件
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)

        # print(f'响应已写入文件 {file_name}')
    else:
        # print(f'请求失败，状态码：{response.status_code}')
        pass


def login():
    # print(111)
    pass


def do_request():
    # 定义要发送的Cookie
    global cookies
    if cookies == None or cookies == "":
        cookies = os.getenv("COOKIES", "")
        if (cookies != ""):
            cookies = json.loads(cookies.replace("'", "\""))
    # 定义目标网址
    url = 'http://wss.gkoudai.com/index.php?m=my&f=index'

    # 发送HTTP GET请求并获取响应
    response = requests.get(url, cookies=cookies)
    write_response_to_html(response)
    return response.text


def analyse_html(html_body):
    global cookies
    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html_body, 'html.parser')
    # 查找相应的元素并提取数据
    soup_tile_title = soup.find("div", class_="tile-title", string="我的任务")
    if soup_tile_title == None:
        cookies = login_get_cookie(config('USERNAME'), config('PASSWORD'))
        # 更新 cookies
        config.set('COOKIES', cookies)
        print("登录过期，已经重新登录")
        return analyse_html(do_request())
    my_tasks = soup_tile_title.find_next_sibling(
        "div", class_="tile-amount").text.strip()
    my_bugs = soup.find("div", class_="tile-title",
                        string="我的BUG").find_next_sibling("div", class_="tile-amount").text.strip()
    my_requirements = soup.find(
        "div", class_="tile-title", string="我的需求").find_next_sibling("div", class_="tile-amount").text.strip()
    unclosed_projects = soup.find(
        "div", class_="tile-title", string="未关闭的项目").find_next_sibling("div", class_="tile-amount").text.strip()

    # 记录数据
    data['my_tasks'] = my_tasks
    data['my_bugs'] = my_bugs
    data['my_requirements'] = my_requirements
    data['unclosed_projects'] = unclosed_projects
    return data


def write_data_to_local(data):
    with open(file_name, "w") as json_file:
        json.dump(data, json_file)
    # print(f"数据已写入文件 {file_name}")


def read_data_from_local(file_name):
    # 从 JSON 文件中读取数据并转换为字典
    with open(file_name, "r") as json_file:
        return json.load(json_file)


def check_and_notify():
    response = do_request()
    new_data = analyse_html(response)
    old_data = read_data_from_local(file_name)
    print("old_data---", old_data)
    print("new_data---", new_data)
    # 如果远程数据有更新才通知
    if Counter(new_data) != Counter(old_data):
        # 数据持久化
        write_data_to_local(new_data)
        show_notice(new_data)


def show_notice(data):
    # 所有具有相同 group 值的通知将被分组在一起，以便用户可以一起查看或关闭它们
    Notifier.notify(f"我的任务: {data['my_tasks']}\n我的BUG: {data['my_bugs']}\n我的需求: {data['my_requirements']}", sound='default',
                    open='http://wss.gkoudai.com/index.php?m=my&f=index')


class MyStatusBarApp(rumps.App):
    def __init__(self):
        super(MyStatusBarApp, self).__init__(
            "My App", icon="/Users/markgosling/Documents/100-Project/02-Python/MyScript/notice_work/notice.png", title="Focus")
        self.menu = [rumps.MenuItem("自动获取禅道信息", callback=self.start_listening),
                     rumps.MenuItem("立即获取禅道信息", callback=self.get_notice),
                     rumps.MenuItem("登录获取 cookies", callback=self.login_get_cookies)]
        self.loop_thread = None
        # 是否已开启监听，当值为 false 时退出程序循环监听
        self.is_running = False
        self.start_listening(None)

    def login_get_cookies(self, _):
        # print(123)
        main()

    def start_listening(self, _):
        print("自动获取禅道信息已开启...")
        if not self.is_running:
            self.is_running = True
            self.loop_thread = threading.Thread(target=self.run_loop)
            self.loop_thread.start()

    def get_notice(self, _):
        check_and_notify()

    def stop_listening(self, _):
        self.is_running = False
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.join()

    def run_loop(self):
        global is_first_init
        while self.is_running:
            # 第一次启动逻辑判断
            if is_first_init:
                check_and_notify()
                is_first_init = False
            time.sleep(5)


if __name__ == "__main__":
    app = MyStatusBarApp()
    app.run()
