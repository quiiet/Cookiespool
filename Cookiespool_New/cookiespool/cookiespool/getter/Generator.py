from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import os
import sys
import json
sys.path.append(os.getcwd())
from cookiespool.cookiespool.my_redis.redis_func import RedisClient
from selenium.webdriver import ChromeOptions 
import time
from cookiespool.cookiespool.utils import get_config
path = '\\getter\\urls.json'

EXCEPTIONS = {
    TimeoutException,
}

url = get_config(path, 'qqmail')
url1 = get_config(path, 'meituan')


class Generator(object):
    def __init__(self, key, value):
        chrome_options= webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 10)
        self.key = key
        self.value = value
        self.db = RedisClient(key, value)


    def one_data(self, i):
        name_list = self.db.usernames()
        vlaue = self.db.get(name_list[i])
        dic = []#假字典
        dic.append(name_list[i])
        dic.append(vlaue)
        return dic


    def get(self, id, passwd):
        cookies = ''
        return cookies


    def login_error(self, url):
        now_url = self.browser.current_url
        if now_url == url:
            return True
        else:
            return False

    
    def run(self):
        for i in range(0, len(self.db.usernames())):
            js = self.one_data(i)
            id = js[0]
            passwd = js[1]
            cookies = self.get(id, passwd)
            print('\n')
            if cookies:
                cookie = json.dumps(cookies)
                print(cookie)
                db = RedisClient('cookies', self.value)
                db.set(id, cookie)
                print(id,'成功存入')
            else:
                print(id, '获取失败返回空')
        print('\n')
        print('-----全部账号处理完成-----')
        print('-----', self.__class__.__name__, '退出-----')
        self.browser.quit()


class QQmailGnerator(Generator):
    def __init__(self, key='accounts', value='qqmail'):
        Generator.__init__(self, key, value)
        self.key = key
        self.value = value
        


    def get(self, username, value):
        try:
            self.browser.get(url)
            time.sleep(2)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qqLoginTab"]'))).click()
            self.browser.switch_to.frame("login_frame")
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="u"]'))).send_keys(username)
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="p"]'))).send_keys(value)
            time.sleep(2)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_button"]'))).click()
            time.sleep(10)
            
        except Exception:
            print('QQmail登录失败')
            return None

        if self.login_error(url):
            print('QQmail账号密码错误或出现验证码')
            print('QQmail获取失败')
            return None
        print('成功登录')
        time.sleep(2)
        print(self.browser.current_url)
        print(os.getcwd())
        with open(os.getcwd()+'\\cookiespool\\getter\\testurls.json', "a") as u:  #保存登陆后的网址便于测试
                                                                                #新建文件而不是在原有文件添加
            tset_url = {"qqmailtest": self.browser.current_url}
            json.dump(tset_url, u)
        try:
            qqmail_cookies = self.browser.get_cookies()
            print('成功获取QQcookies')
            print(qqmail_cookies)
            return qqmail_cookies
        except Exception:
            print('QQmail获取失败')
            return None
        
    
class MeituanGnerator(Generator):
    def __init__(self, key='accounts', value='meituan'):
        Generator.__init__(self, key, value)
        self.key = key
        self.value = value
        self.browser.maximize_window()
        self.actions = ActionChains(self.browser)
            
        
    def track(self, distance):
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.5
        # 初速度
        # v = 0
        v = 0
        while current < distance:
            if current < mid:
                # 加速度为正2
            # a_b = 8
                a = 5
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a_b * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        print(track)
        return track


    def get(self, id, passwd):
        try:
            #登录
            self.browser.get(url1)
            time.sleep(2)
            self.wait.until(EC.element_to_be_clickable((By.ID, 'J-third-tencent'))).click()
            time.sleep(5)
            self.browser.switch_to_frame('ptlogin_iframe')
            self.actions.move_by_offset(xoffset=487, yoffset=361).click().perform()
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'inputstyle'))).send_keys(id)
            time.sleep(2)
            self.wait.until(EC.presence_of_element_located((By.ID, 'p'))).send_keys(passwd)
            time.sleep(2)
            self.wait.until(EC.element_to_be_clickable((By.ID, 'login_button'))).click()
            time.sleep(5)
        except TimeoutException:
            print('登陆失败')
            return None
        time.sleep(5)
        if self.browser.current_url == url1:  #表示出现验证码
            try:
                self.actions.reset_actions()    
                time.sleep(2)
                # 等待图片加载出来
                WebDriverWait(self.browser, 5, 0.5).until(
                    EC.presence_of_element_located((By.ID, "tcaptcha_drag_button"))
                )
                try:
                    button = button = self.browser.find_element_by_id('tcaptcha_drag_button')
                except Exception as e:
                    print( 'get button failed: ', e)
                time.sleep(2)
                self.actions.click_and_hold(button).perform()
                time.sleep(5)
                for i in range(6):
                        
                    # 清除之前的action
                    self.actions.reset_actions()
                    #模拟轨迹方程
                    track = self.track(158)
                    #开始模拟拖拽
                    for i in track:
                        #y轴不偏移，x轴持续滑动
                        self.actions.move_by_offset(xoffset=i, yoffset=0).perform()
                        self.actions.reset_actions()
                    time.sleep(0.5)
                    #释放鼠标
                    self.actions.release().perform()
                    time.sleep(5)
                time.sleep(5)
                if self.login_error('https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=code&redirect_uri=https%3A%2F%2Fpassport.meituan.com%2Faccount%2Fcallback%2Ftencent&client_id=214506'):
                    print('验证码破解失败')
                    return None
                print('成功登录')
                try:
                    meituan_cookies = self.browser.get_cookies()
                    print('成功获取meituancookies')
                    print(meituan_cookies)
                    return meituan_cookies
                except TimeoutException:
                    print('meituan获取失败')
                    return None
            except TimeoutException:
                print('验证码破解失败')
        
        try:
            meituan_cookies = self.browser.get_cookies()
            print('成功获取meituancookies')
            print(meituan_cookies)
            return meituan_cookies
        except:
            print('美团cookies获取失败')
        '''
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header-search-input'))).send_keys('火锅')
        time.sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/div[1]/button'))).click()
        time.sleep(3)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'list-item-desc')))
    
        #一页还是比较多，就不翻页
        '''

