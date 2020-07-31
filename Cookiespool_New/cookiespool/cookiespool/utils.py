import os
import sys
import json

strs = os.path.dirname(__file__)#获取路径

def get_config(file_path, args):
    complete_path = strs + file_path
    with open(complete_path, "r") as f:
        
        text = f.read()
    js = json.loads(text)
    got = js.get(args)
    f.close()
    return got
'''
def get_user_config(file_path, name, i):
    complete_path = strs + file_path
    with open(complete_path, "r") as f:
        text = f.read()
    js = json.loads(text)
    got = js.get(name)(args)
    return got
'''