# 目前只适配了 Mac OS
# 测试平台：Mac OS 14.0
# Python 版本：3.11.4
# todo 我正在完成任务的时候不要弹出
import requests
from bs4 import BeautifulSoup
from pync import Notifier
from decouple import config
import rumps
import json
import time
import os

data = dict()
file_name = "work_data.json"


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

        print(f'响应已写入文件 {file_name}')
    else:
        print(f'请求失败，状态码：{response.status_code}')


def do_request():
    # 定义要发送的Cookie
    # cookies = json.loads(config('COOKIES'))
    cookies = string_to_dict(config('COOKIES_FROM_BROWSER'))
    # 定义目标网址
    url = 'http://wss.gkoudai.com/index.php?m=my&f=index'

    # 发送HTTP GET请求并获取响应
    response = requests.get(url, cookies=cookies)
    return response.text


def analyse_html(html_body):
    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html_body, 'html.parser')

    # 查找相应的元素并提取数据
    my_tasks = soup.find("div", class_="tile-title",
                         string="我的任务").find_next_sibling("div", class_="tile-amount").text.strip()
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
    print(f"数据已写入文件 {file_name}")


def read_data_from_local(file_name):
    # 从 JSON 文件中读取数据并转换为字典
    with open(file_name, "r") as json_file:
        return json.load(json_file)


def check_and_notify():
    response = do_request()
    analyse_html(response)


def show_notice(data):
    # 所有具有相同 group 值的通知将被分组在一起，以便用户可以一起查看或关闭它们
    Notifier.notify(f"我的任务: {data['my_tasks']}\n我的BUG: {data['my_bugs']}\n我的需求: {data['my_requirements']}", sound='default',
                    open='http://wss.gkoudai.com/index.php?m=my&f=index')


if __name__ == "__main__":
    while True:
        response = do_request()
        work_data = analyse_html(response)
        # 第一次启动逻辑判断
        if data['my_tasks'] != "0" or data['my_bugs'] != "0" or data['my_requirements'] != "0":
            show_notice(work_data)
        # 数据持久化
        write_data_to_local(data)
        # 等待5分钟
        time.sleep(300)
