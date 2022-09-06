from flask import Blueprint
import sys
import time
import database

sys.path.append(".")
app = Blueprint('app',__name__)

# ==========OLD==========

clip_list = []


@app.route('/')  # 装饰器，url，路由
def index():  # 试图函数
    return 'this is AirClip'


@app.route('/say_hello/<name>')  # 装饰器，url，路由
def say_hello(name):  # 试图函数

    return 'hello world,I am your friend %s' % name


@app.route('/new_clip/<name>')  # 装饰器，url，路由
def new_clip(name):  # 试图函数
    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    clip_list.append({'time': curtime, 'content': name})
    database.app_airclip_add_item(curtime, name, 'test')
    return 'new_clip: %s' % name


@app.route('/get_clip/')  # 装饰器，url，路由
def get_clip():  # 试图函数

    ret = clip_list.copy()
    ret.reverse()

    l = database.app_airclip_show_item()
    print(l)

    new_ret = []
    for i in l:
        new_ret.append({'time': i[0], 'content': i[1]})

    new_ret.reverse()

    return new_ret
