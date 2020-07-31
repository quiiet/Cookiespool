from flask import Flask, g
import sys
import os
sys.path.append(os.getcwd())
from cookiespool.cookiespool.utils import get_config
from cookiespool.cookiespool.my_redis.redis_func import RedisClient


app = Flask(__name__)

GENERATOR_MAP = {
    'qqmail': ' QQmail',
}

def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
    return g


@app.route('/')
def index():
    return '<h2>Welcome to The CookiesPool</h2>'


@app.route('/<website>/random')
def random(website):
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies



    
