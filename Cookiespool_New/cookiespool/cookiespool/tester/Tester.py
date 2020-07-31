import requests
from requests.exceptions import ConnectionError, ConnectTimeout
import json
from json import JSONDecodeError
import sys
import os
import pickle
sys.path.append(os.getcwd())
from cookiespool.cookiespool.utils import get_config
path = '\\getter\\urls.json'
path2 = '\\getter\\testurls.json'
from cookiespool.cookiespool.my_redis.redis_func import RedisClient
from requests import session

Exceptions = (
    ConnectTimeout,
    ConnectionError,
    JSONDecodeError,
    TypeError,
)

class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)


    def test(self, username, cookies):
        print('正在测试cookies', '用户名', username)
        try:
            cookie_loads = json.loads(cookies)
        except Exceptions:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            tmp_cookies = requests.cookies.RequestsCookieJar()
            sess = requests.session()
            for item in cookie_loads:
                tmp_cookies.set(item["name"], item["value"])
            sess.cookies.update(tmp_cookies)
            test_url = get_config(path, 'meituantest')
            r = sess.get(test_url)
            #response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if r.status_code == 200:
                print('Cookies有效', username)
                print('部分测试结果：', r.text[0:50])
            else:
                print(r.status_code, r.headers)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('adwadwad')
            print('发生异常', e.args)




    def run(self):
        cookies_group = self.cookies_db.all()
        for username, cookies in cookies_group.items():
            self.test(username, cookies)


class QQmailValidTester(ValidTester):
    def __init__(self, website='qqmail'):
        self.website = website
        ValidTester.__init__(self, website)


    
class MeituanValidTester(ValidTester):
    def __init__(self, website='meituan'):
        self.website = website
        ValidTester.__init__(self, website)


    

