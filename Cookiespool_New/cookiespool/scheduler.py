import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + '\\cookiespool\\cookiespool\\my_reids')
from cookiespool.cookiespool.my_redis.redis_func import RedisClient
from cookiespool.cookiespool.getter.Generator import *
from cookiespool.cookiespool.tester.Tester import *
from cookiespool.cookiespool.server.Api import app
import time
from multiprocessing import Process
from cookiespool.cookiespool.utils import get_config
path = '\\settings.json'


CYCLE = 20
websites = [
    'QQmail',
    'Meituan'
]

HOST = get_config(path, 'HOST')
PORT = get_config(path, 'PORT')
TESTER_ENABLE = get_config(path, 'TESTER_ENABLE')
GENERATOR_ENABLE = get_config(path, 'GENERATOR_ENABLE')
API_ENABLE = get_config(path, 'API_ENABLE')

class Scheduler(object):
    @staticmethod
    def test_cookies(cycle=CYCLE):
        while True:
            print('\n')
            print('测试器开始执行')
            try:
                for web in websites:
                    print('-----', web, '测试器开始执行-----')
                    cls_name = web + 'ValidTester'
                    tester = eval(cls_name + '(' + ')')
                    tester.run()
                    print(web, 'Cookies检测完成')
                    print('-----', web, '测试器退出-----')
                    del tester
                    time.sleep(cycle / 2)
            except Exception as e:
                print(e.args)
                time.sleep(CYCLE / 2)


    @staticmethod
    def generat_cookies(cycle=CYCLE):
        print('生成器开始执行')
        try:
            for web in websites:
                print('-----', web + 'Gnerator', '生成器开始运行-----')
                cls_name = web + 'Gnerator'
                tester = eval(cls_name + '(' + ')')
                tester.run()
                print('-----', web + 'Gnerator', '生成器退出-----')
                print('\n')
                time.sleep(cycle)
        except Exception as e:
            print(e.args)


    @staticmethod
    def api_cookies():
        print('API接口开始运行')
        app.run(host=HOST, port=PORT)


    def run(self):
        print('Cookies池开始运行\n')
        
        time.sleep(2)
        if TESTER_ENABLE == 1:
            tester_process = Process(target=Scheduler.test_cookies)
            tester_process.start()


        if GENERATOR_ENABLE == 1:
            getter_process = Process(target=Scheduler.generat_cookies)
            getter_process.start()

        if API_ENABLE == 1:
            api_process = Process(target=Scheduler.api_cookies)
            api_process.start()



