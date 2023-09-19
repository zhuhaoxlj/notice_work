import requests
import json


def write_text_to_html(text):
    # 检查响应状态码，确保请求成功
    # 定义文件名
    file_name = 'cookies.html'
    # 将响应内容写入文件
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f'响应已写入文件 {file_name}')


url = 'http://wss.gkoudai.com/index.php?m=user&f=login'
username = ''
password = ''
# 创建一个session,作用会自动保存cookie
session = requests.session()
data = {
    'account': username,
    'password': password,
    'keepLogin': 1
}
# 使用session发起post请求来获取登录后的cookie,cookie已经存在session中
response = session.post(url=url, data=data)

# 用session给个人主页发送请求，因为session中已经有cookie了
index_url = 'http://wss.gkoudai.com/index.php?m=my&f=index'
cookies = session.get(url=index_url)

# 将Cookies转换为字符串
cookies_str = '; '.join([f"{cookie.name}={cookie.value}" for cookie in cookies.cookies])
print(cookies_str)
write_text_to_html(cookies.text)
