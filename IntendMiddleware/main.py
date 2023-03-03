from flask import Flask, request
import time
import requests
import json
app = Flask("IntendMiddleware")


# ==========Configuration==========
IS_DEBUG = True
SERVER_IP = '0.0.0.0'
SERVER_PORT = '5000'
GPT_URL = 'http://220.249.18.254:31999/gpt/v1/completion'

# "app":["com.huawei.appmarket","com.baidu.BaiduMap","com.cainiao.wireless","com.ss.android.ugc.aweme","com.dianping.v1","com.sdu.didi.psnger","me.ele","com.taobao.trip","com.autonavi.minimap","com.tencent.tmgp.pubgmhd","com.jingdong.app.mall","com.smile.gifmaker","com.sankuai.meituan","com.mt.mtxx.mtxx","com.sankuai.movie","com.xunmeng.pinduoduo","com.tencent.mobileqq","com.tencent.qqmusic","com.taobao.taobao","com.tencent.mm","com.netease.cloudmusic","ctrip.android.view","com.xt.retouch","com.youku.phone","com.eg.android.AlipayGphone","battymole.trainticket","com.qiyi.video"],

# ==========Utils==========


def printDebugInfo(*args, level='info'):
    if IS_DEBUG:
        print("\n=====level=", level, "DEBUG=====")
        for i in args:
            print(i)
        print("*****level=", level, "DEBUG*****\n")


# ==========Function==========

@app.route('/hello', methods=['GET', 'POST'])
def response_hello():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@app.route('/test', methods=['GET', 'POST'])
def response_test():
    ret = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
    data = {
        "model": "text-davinci-003",
        "temperature": 0.5,
        "prompt": "Hello!"
    }
    res = requests.post(GPT_URL, data=json.dumps(data))
    ret = json.loads(res.text)[0].strip()
    printDebugInfo(ret)

    return ret


@app.route('/intend/v1', methods=['POST'])
def response_intend_v1():
    para = json.loads(request.data)
    printDebugInfo(para)

    # prompt = 'I have '
    prompt = '在我的手机里的应用程序有'
    for i in para["app"]:
        prompt += i+', '
    # prompt += '拍拍助手 in my phone.'
    prompt += '拍拍助手。'

    # prompt += " When i mentioned the keyword '{}', which applications in my smartphone do I intent to use? Please list all the applications I intent to use completely and tell me why. ".format(
    #     para["keyword"])
    prompt += " 用json的list的格式表示，当我提到“{}”时所有我手机里的应用程序，我大概率会用到的几个是哪些，按用到的概率从高到低，最多列出5个应用程序。".format(
        para["keyword"])
    # prompt += " 当我说“{}”时所有在我手机里有的我最有可能用到的一个应用程序是哪一个。注意不要列出我手机里没有的应用程序。只告诉我应用程序的名称。".format(
    #     para["keyword"])
    printDebugInfo(prompt)

    data = {
        "model": "text-davinci-003",
        "temperature": 0.8,
        "max_tokens": 50,
        "prompt": prompt
    }
    res = requests.post(GPT_URL, data=json.dumps(data))
    ret = json.loads(res.text)[0].strip()
    # ret = res.text
    printDebugInfo(ret)

    return ret


APP_LABEL_DICT = {
    '新闻资讯': ['浏览器', '今日头条', '百度APP', '微博'],
    '聊天': ['微信'],
    '社交': ['微信', '抖音', '微博', '知乎'],
    '支付': ['微信', '支付宝'],
    '短视频': ['抖音'],
    '搜索': ['百度APP'],
    '地图': ['百度APP', '高德地图', '百度地图'],
    '知识问答': ['百度APP', '知乎'],
    '网页浏览': ['百度APP'],
    '在线购物': ['淘宝', '京东', '拼多多'],
    '外卖': ['美团'],
    '酒店': ['美团'],
    '旅游': ['美团'],
    '美食': ['美团'],
    '导航': ['高德地图', '百度地图'],
    '路线规划': ['高德地图', '百度地图'],
    '生活服务': ['支付宝'],
    '理财': ['支付宝'],
    '动漫': ['哔哩哔哩', '爱奇艺'],
    '视频': ['爱奇艺', '哔哩哔哩'],
    '电影': ['爱奇艺'],
    '电视剧': ['爱奇艺'],
    '综艺': ['爱奇艺'],
    '音乐播放': ['酷狗音乐', 'QQ音乐', '网易云音乐'],
    '在线音乐': ['酷狗音乐', 'QQ音乐', '网易云音乐']
}


@app.route('/intend/v2', methods=['POST'])
def response_intend_v2():
    para = json.loads(request.data)
    printDebugInfo(para)

    label = ''
    for i in APP_LABEL_DICT:
        label += i + ','

    prompt = "对需求进行如下归类：{}。当我在搜索框中输入“{}”时，列出我最有可能有哪几类的需求，最多列出5个并且不要给出任何解释。".format(
        label, para["keyword"])

    # prompt += " When i mentioned the keyword '{}', which applications in my smartphone do I intent to use? Please list all the applications I intent to use completely and tell me why. ".format(
    #     para["keyword"])
    # prompt += " 用json的list的格式表示，当我提到“{}”时所有我手机里的应用程序，我大概率会用到的几个是哪些，按用到的概率从高到低，最多列出5个应用程序。".format(
    #     para["keyword"])
    # prompt += " 当我说“{}”时所有在我手机里有的我最有可能用到的一个应用程序是哪一个。注意不要列出我手机里没有的应用程序。只告诉我应用程序的名称。".format(
    #     para["keyword"])
    printDebugInfo(prompt)

    data = {
        "model": "text-davinci-003",
        "temperature": 0.8,
        "max_tokens": 50,
        "prompt": prompt
    }
    res = requests.post(GPT_URL, data=json.dumps(data))
    ret = json.loads(res.text)[0].strip()
    # ret = res.text
    printDebugInfo(ret)

    return ret


# =====Start Flask=====

app.run(debug=IS_DEBUG, host=SERVER_IP, port=SERVER_PORT)
