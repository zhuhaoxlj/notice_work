from urllib.parse import urljoin
from lxml import etree
import browser_cookie3
import requests


def get_cookie():
    url = 'http://wss.gkoudai.com/index.php?m=user&f=login'
    cookies = browser_cookie3.chrome(domain_name='wss.gkoudai.com')
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
    response = session.post(url=url, data=data, cookies=cookies)
    cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)
    return cookies_dict


get_cookie()
