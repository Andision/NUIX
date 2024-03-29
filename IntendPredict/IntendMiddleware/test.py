from email.policy import default
import json
import requests


def get_top(d, top):
    ret = []
    for i in sorted(d.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if top == 0:
            break
        top -= 1
        ret.append(i)

    return [i[0] for i in ret]


def send_to_gpt(keyword):
    # para = json.loads(request.data)
    # print(para)
    label = ''
    for i in APP_LABEL_DICT:
        label += i + ','

    prompt = "对需求进行如下归类：{}。当我在搜索框中输入“{}”时，列出我最有可能有哪几类的需求，每个需求之间用|隔开，按照我可能使用的概率从高到底排列，最多列出5个并且不要给出任何解释。".format(
        label, keyword)

    # prompt += " When i mentioned the keyword '{}', which applications in my smartphone do I intent to use? Please list all the applications I intent to use completely and tell me why. ".format(
    #     para["keyword"])
    # prompt += " 用json的list的格式表示，当我提到“{}”时所有我手机里的应用程序，我大概率会用到的几个是哪些，按用到的概率从高到低，最多列出5个应用程序。".format(
    #     para["keyword"])
    # prompt += " 当我说“{}”时所有在我手机里有的我最有可能用到的一个应用程序是哪一个。注意不要列出我手机里没有的应用程序。只告诉我应用程序的名称。".format(
    #     para["keyword"])
    # print(prompt)

    data = {
        "model": "text-davinci-003",
        "temperature": 0.8,
        "max_tokens": 50,
        "prompt": prompt
    }

    isTimeout = True

    while isTimeout:

        try:
            res = requests.post(GPT_URL, data=json.dumps(data))
            ret = json.loads(res.text)[0].strip().split('|')
            isTimeout = False
        except:
            isTimeout = True

    # ret = res.text
    # print(ret)
    return ret


APP = ["浏览器", "微信", "抖音", "百度", "淘宝", "京东", "拼多多", "今日头条", "美团", "高德地图",
       "支付宝", "哔哩哔哩", "微博", "酷狗音乐", "爱奇艺", "QQ音乐", "百度地图", "网易云音乐", "知乎"]
SAMPLE = {
    "高德地图": [
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "五道口地铁站",
            "意图说明": "搜索地点"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "五道口椒麻小馆",
            "意图说明": "搜索路线"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "奶茶",
            "意图说明": "搜索附近服务"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "双清公寓",
            "意图说明": "搜索地点"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "柏拉图咖啡馆",
            "意图说明": "搜索地点"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "清华大学东北门",
            "意图说明": "搜索地点"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "青悦城",
            "意图说明": "搜索开车路线"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "西施故里",
            "意图说明": "搜索开车路线"
        },
        {
            "App": "高德地图",
            "任务类型": "搜索",
            "文本输入": "圆明园地铁站",
            "意图说明": "搜索路线"
        }
    ],
    "微信": [
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "二姨",
            "意图说明": "搜索联系人"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "行在清华",
            "意图说明": "搜索微信公众号"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "清华大学在线服务",
            "意图说明": "搜索微信公众号"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "食堂开伙时间",
            "意图说明": "搜索微信公众号"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "清华专线",
            "意图说明": "搜索微信公众号"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "X老师",
            "意图说明": "搜索联系人"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "Friday",
            "意图说明": "搜索群聊"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "晚饭",
            "意图说明": "发消息"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "小五爷园",
            "意图说明": "搜索公众号"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "ttttt",
            "意图说明": "搜索联系人"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "项目书.doc",
            "意图说明": "搜索文件"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "明天在哪里",
            "意图说明": "搜索聊天记录"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "生日快乐",
            "意图说明": "搜索聊天记录"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "周",
            "意图说明": "搜索联系人"
        },
        {
            "App": "微信",
            "任务类型": "搜索",
            "文本输入": "陈",
            "意图说明": "搜索陈姓联系人"
        }
    ],
    "爱奇艺": [
        {
            "App": "爱奇艺",
            "任务类型": "搜索",
            "文本输入": "狂飙",
            "意图说明": "搜索电视剧"
        },
        {
            "App": "爱奇艺",
            "任务类型": "搜索",
            "文本输入": "三体",
            "意图说明": "搜索电视剧"
        }
    ],
    "新浪微博": [
        {
            "App": "新浪微博",
            "任务类型": "搜索",
            "文本输入": "狂飙",
            "意图说明": "搜索电视剧相关新闻"
        },
        {
            "App": "新浪微博",
            "任务类型": "搜索",
            "文本输入": "ChatGPT",
            "意图说明": "搜索新事物"
        },
        {
            "App": "新浪微博",
            "任务类型": "搜索",
            "文本输入": "张颂文",
            "意图说明": "搜索明星相关信息"
        },
        {
            "App": "新浪微博",
            "任务类型": "搜索",
            "文本输入": "胡鑫宇",
            "意图说明": "搜索热点事件"
        },
        {
            "App": "新浪微博",
            "任务类型": "搜索",
            "文本输入": "柏浪涛",
            "意图说明": "搜索法考老师"
        }
    ],
    "safari": [
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "胃痛应该吃什么药",
            "意图说明": "搜索生活常识"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "G302",
            "意图说明": "搜索车次信息"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "颈椎病治疗",
            "意图说明": "搜索生活常识"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "左下腹疼痛",
            "意图说明": "搜索生活常识"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "阳了吃什么",
            "意图说明": "搜索健康疾病相关内容"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "健听女孩",
            "意图说明": "搜索电影资料"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "狂飙主演",
            "意图说明": "搜索电视剧资料"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "苹果官网",
            "意图说明": "搜索电子产品"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "巨齿鲨2",
            "意图说明": "搜索新电影资讯"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "杜伏威",
            "意图说明": "搜索历史人物"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "宿建德江",
            "意图说明": "搜索文学作品"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "貔貅",
            "意图说明": "搜索文学常识"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "相邦吕不韦造",
            "意图说明": "搜索文物知识"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "满江红票房",
            "意图说明": "搜索电影资讯"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "山在线阅读",
            "意图说明": "搜索小说原文"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "富弼",
            "意图说明": "搜索历史人物"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "证伪理论",
            "意图说明": "搜索哲学概念"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "如何让电脑屏幕常亮",
            "意图说明": "搜索电脑知识"
        },
        {
            "App": "safari",
            "任务类型": "搜索",
            "文本输入": "严打",
            "意图说明": "搜索专有名词"
        }
    ],
    "美团": [
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "和府捞面",
            "意图说明": "搜索外卖服务"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "肯德基",
            "意图说明": "搜索外卖服务"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "麦当劳",
            "意图说明": "搜索外卖服务"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "麻辣烫",
            "意图说明": "搜索外卖服务"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "kfc",
            "意图说明": "搜索商铺"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "米线",
            "意图说明": "搜索食物"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "煲仔饭",
            "意图说明": "搜索美食外卖"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "鸡公煲",
            "意图说明": "点外卖"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "炸鸡",
            "意图说明": "点外卖"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "奶茶",
            "意图说明": "搜索奶茶推荐"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "电影院",
            "意图说明": "搜索附近电影院"
        },
        {
            "App": "美团",
            "任务类型": "搜索",
            "文本输入": "酒店",
            "意图说明": "寻找附近酒店"
        }
    ],
    "12306": [
        {
            "App": "12306",
            "任务类型": "搜索",
            "文本输入": "北京 天津",
            "意图说明": "搜索出行信息"
        },
        {
            "App": "12306",
            "任务类型": "搜索",
            "文本输入": "北京",
            "意图说明": "搜索目的地车次"
        },
        {
            "App": "12306",
            "任务类型": "搜索",
            "文本输入": "上海",
            "意图说明": "搜索高铁票"
        }
    ],
    "知乎": [
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "颈椎病治疗",
            "意图说明": "搜索生活常识"
        },
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "股票发行注册制",
            "意图说明": "搜索相关新闻"
        },
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "幻方量化",
            "意图说明": "搜索相关新闻"
        },
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "狂飙",
            "意图说明": "搜索电视剧相关新闻"
        },
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "清华大学新雅书院",
            "意图说明": "搜索专业领域内容"
        },
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "国家电网",
            "意图说明": "搜索就业信息"
        },
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "chatGPT",
            "意图说明": "搜索信息"
        },
        {
            "App": "知乎",
            "任务类型": "搜索",
            "文本输入": "公务员考试",
            "意图说明": "了解考试的相关信息"
        }
    ],
    "哔哩哔哩": [
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "b站年度报告",
            "意图说明": "搜索视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "csgo",
            "意图说明": "搜索短视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "战地2042",
            "意图说明": "搜索短视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "俄乌冲突",
            "意图说明": "搜索短视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "美食作家王刚",
            "意图说明": "搜索up主"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "麻将规则",
            "意图说明": "搜索生活常识"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "大连小王爱踢球",
            "意图说明": "搜索搞笑视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "中国奇谭",
            "意图说明": "搜索动画"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "饲养员小谢",
            "意图说明": "搜索搞笑视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "土耳其",
            "意图说明": "搜索新闻相关视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "月亮要早睡",
            "意图说明": "搜索up主"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "九转大肠",
            "意图说明": "搜索相关视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "郑钦文",
            "意图说明": "搜索人物相关视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "流浪地球2片尾",
            "意图说明": "搜索电影相关的视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "焦裕禄",
            "意图说明": "搜索人物相关的视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "土耳其地震",
            "意图说明": "搜索新闻"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "刘培茄",
            "意图说明": "搜索搞笑视频"
        },
        {
            "App": "哔哩哔哩",
            "任务类型": "搜索",
            "文本输入": "fgo",
            "意图说明": "搜索二创视频"
        }
    ],
    "QQ音乐": [
        {
            "App": "QQ音乐",
            "任务类型": "搜索",
            "文本输入": "qq音乐年度报告",
            "意图说明": "搜索年度报告"
        },
        {
            "App": "QQ音乐",
            "任务类型": "搜索",
            "文本输入": "搁浅",
            "意图说明": "搜索歌曲"
        },
        {
            "App": "QQ音乐",
            "任务类型": "搜索",
            "文本输入": "林俊杰",
            "意图说明": "搜索歌手"
        },
        {
            "App": "QQ音乐",
            "任务类型": "搜索",
            "文本输入": "陶喆",
            "意图说明": "搜索音乐人"
        },
        {
            "App": "QQ音乐",
            "任务类型": "搜索",
            "文本输入": "丁世光",
            "意图说明": "搜搜音乐人"
        }
    ],
    "网易云音乐": [
        {
            "App": "网易云音乐",
            "任务类型": "搜索",
            "文本输入": "网易云年度报告",
            "意图说明": "搜索年度报告"
        },
        {
            "App": "网易云音乐",
            "任务类型": "搜索",
            "文本输入": "只因你太美",
            "意图说明": "搜索歌曲"
        },
        {
            "App": "网易云音乐",
            "任务类型": "搜索",
            "文本输入": "我不曾忘记",
            "意图说明": "搜索音乐"
        },
        {
            "App": "网易云音乐",
            "任务类型": "搜索",
            "文本输入": "赵雷",
            "意图说明": "搜索歌手"
        },
        {
            "App": "网易云音乐",
            "任务类型": "搜索",
            "文本输入": "深海",
            "意图说明": "搜索音乐"
        }
    ],
    "京东": [
        {
            "App": "京东",
            "任务类型": "搜索",
            "文本输入": "小米蓝牙耳机",
            "意图说明": "搜索商品"
        },
        {
            "App": "京东",
            "任务类型": "搜索",
            "文本输入": "颈椎枕",
            "意图说明": "搜索商品"
        },
        {
            "App": "京东",
            "任务类型": "搜索",
            "文本输入": "机械硬盘",
            "意图说明": "搜索相关产品"
        }
    ],
    "今日头条": [
        {
            "App": "今日头条",
            "任务类型": "搜索",
            "文本输入": "chatgpt",
            "意图说明": "搜索新闻"
        }
    ],
    "牛客网": [
        {
            "App": "牛客网",
            "任务类型": "搜索",
            "文本输入": "腾讯面经",
            "意图说明": "搜索信息"
        }
    ],
    "豆瓣阅读": [
        {
            "App": "豆瓣阅读",
            "任务类型": "搜索",
            "文本输入": "三体",
            "意图说明": "搜索电子书"
        }
    ],
    "豆瓣": [
        {
            "App": "豆瓣",
            "任务类型": "搜索",
            "文本输入": "满江红",
            "意图说明": "搜索电影"
        },
        {
            "App": "豆瓣",
            "任务类型": "搜索",
            "文本输入": "无名",
            "意图说明": "搜索电影"
        },
        {
            "App": "豆瓣",
            "任务类型": "搜索",
            "文本输入": "流浪地球2",
            "意图说明": "搜索电影"
        },
        {
            "App": "豆瓣",
            "任务类型": "搜索",
            "文本输入": "阿凡达",
            "意图说明": "搜索电影"
        },
        {
            "App": "豆瓣",
            "任务类型": "搜索",
            "文本输入": "狂飙",
            "意图说明": "搜索电视剧相关评论"
        }
    ],
    "腾讯视频": [
        {
            "App": "腾讯视频",
            "任务类型": "搜索",
            "文本输入": "三体",
            "意图说明": "搜索电视剧"
        }
    ],
    "东方航空": [
        {
            "App": "东方航空",
            "任务类型": "搜索",
            "文本输入": "昆明-北京",
            "意图说明": "填写目的地"
        }
    ],
    "百度贴吧": [
        {
            "App": "百度贴吧",
            "任务类型": "搜索",
            "文本输入": "地狱笑话",
            "意图说明": "搜索相关回帖"
        }
    ],
    "微博": [
        {
            "App": "微博",
            "任务类型": "搜索",
            "文本输入": "wbgvsjdg",
            "意图说明": "搜索体育比赛结果"
        },
        {
            "App": "微博",
            "任务类型": "搜索",
            "文本输入": "周杰伦新歌",
            "意图说明": "搜索娱乐资讯"
        },
        {
            "App": "微博",
            "任务类型": "搜索",
            "文本输入": "湖人",
            "意图说明": "搜索体育相关新闻"
        },
        {
            "App": "微博",
            "任务类型": "搜索",
            "文本输入": "土耳其",
            "意图说明": "搜索新闻"
        }
    ],
    "大众点评": [
        {
            "App": "大众点评",
            "任务类型": "搜索",
            "文本输入": "海淀川菜",
            "意图说明": "搜索美食"
        },
        {
            "App": "大众点评",
            "任务类型": "搜索",
            "文本输入": "德扑",
            "意图说明": "搜索娱乐场所"
        },
        {
            "App": "大众点评",
            "任务类型": "搜索",
            "文本输入": "酸菜鱼",
            "意图说明": "搜索附近美食"
        }
    ],
    "虎扑": [
        {
            "App": "虎扑",
            "任务类型": "搜索",
            "文本输入": "湖人",
            "意图说明": "搜索赛事"
        },
        {
            "App": "虎扑",
            "任务类型": "搜索",
            "文本输入": "湖人",
            "意图说明": "搜索体育相关新闻"
        },
        {
            "App": "虎扑",
            "任务类型": "搜索",
            "文本输入": "浓眉",
            "意图说明": "搜索体育相关新闻"
        }
    ],
    "淘宝": [
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "每日坚果",
            "意图说明": "搜索商品"
        },
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "磁吸手机壳",
            "意图说明": "搜索商品"
        },
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "羽绒服",
            "意图说明": "搜索商品"
        },
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "行李箱20寸",
            "意图说明": "搜索商品"
        },
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "Salomon",
            "意图说明": "搜索品牌"
        },
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "情人节礼物",
            "意图说明": "搜索礼物"
        },
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "行李箱",
            "意图说明": "搜索生活用品"
        },
        {
            "App": "淘宝",
            "任务类型": "搜索",
            "文本输入": "键盘",
            "意图说明": "搜索商品"
        }
    ],
    "支付宝": [
        {
            "App": "支付宝",
            "任务类型": "搜索",
            "文本输入": "地铁",
            "意图说明": "搜索子工具"
        }
    ],
    "携程": [
        {
            "App": "携程",
            "任务类型": "搜索",
            "文本输入": "北京",
            "意图说明": "搜索出行票务信息"
        },
        {
            "App": "携程",
            "任务类型": "搜索",
            "文本输入": "酒店",
            "意图说明": "搜索旅行居住地"
        },
        {
            "App": "携程",
            "任务类型": "搜索",
            "文本输入": "宁波",
            "意图说明": "购买车票"
        }
    ],
    "keep": [
        {
            "App": "keep",
            "任务类型": "搜索",
            "文本输入": "上肢力量",
            "意图说明": "搜索健身课程"
        }
    ],
    "脉脉": [
        {
            "App": "脉脉",
            "任务类型": "搜索",
            "文本输入": "国家电网",
            "意图说明": "搜索就业信息"
        }
    ],
    "百度地图": [
        {
            "App": "百度地图",
            "任务类型": "搜索",
            "文本输入": "上海15号线-永德路地铁站",
            "意图说明": "搜索地点"
        },
        {
            "App": "百度地图",
            "任务类型": "搜索",
            "文本输入": "虹桥地铁站",
            "意图说明": "搜索地点"
        }
    ],
    "得物": [
        {
            "App": "得物",
            "任务类型": "搜索",
            "文本输入": "Air Force 1",
            "意图说明": "搜索球鞋"
        }
    ],
    "直播吧": [
        {
            "App": "直播吧",
            "任务类型": "搜索",
            "文本输入": "东契奇",
            "意图说明": "搜索相关新闻"
        }
    ],
    "小红书": [
        {
            "App": "小红书",
            "任务类型": "搜索",
            "文本输入": "秋招",
            "意图说明": "搜索信息"
        },
        {
            "App": "小红书",
            "任务类型": "搜索",
            "文本输入": "新加坡签证",
            "意图说明": "搜索出游准备"
        },
        {
            "App": "小红书",
            "任务类型": "搜索",
            "文本输入": "冬天羽绒服推荐",
            "意图说明": "搜索商品推荐"
        }
    ],
    "天眼查": [
        {
            "App": "天眼查",
            "任务类型": "搜索",
            "文本输入": "中国国际金融股份有限公司",
            "意图说明": "搜索公司"
        }
    ],
    "网易有道词典": [
        {
            "App": "网易有道词典",
            "任务类型": "搜索",
            "文本输入": "hypophrenia",
            "意图说明": "搜索单词"
        }
    ],
    "携程旅行": [
        {
            "App": "携程旅行",
            "任务类型": "搜索",
            "文本输入": "昆明",
            "意图说明": "搜索机票"
        }
    ],
    "饿了么": [
        {
            "App": "饿了么",
            "任务类型": "搜索",
            "文本输入": "小龙虾",
            "意图说明": "搜索食品"
        },
        {
            "App": "饿了么",
            "任务类型": "搜索",
            "文本输入": "米粉",
            "意图说明": "搜索外卖"
        }
    ],
    "App Store": [
        {
            "App": "App Store",
            "任务类型": "搜索",
            "文本输入": "音游",
            "意图说明": "搜索游戏"
        },
        {
            "App": "App Store",
            "任务类型": "搜索",
            "文本输入": "半月谈",
            "意图说明": "下载软件"
        },
        {
            "App": "App Store",
            "任务类型": "搜索",
            "文本输入": "训记",
            "意图说明": "下载软件"
        },
        {
            "App": "App Store",
            "任务类型": "搜索",
            "文本输入": "腾讯会议",
            "意图说明": "下载软件"
        }
    ],
    "微信读书": [
        {
            "App": "微信读书",
            "任务类型": "搜索",
            "文本输入": "三体",
            "意图说明": "搜索书籍"
        }
    ],
    "Spotify": [
        {
            "App": "Spotify",
            "任务类型": "搜索",
            "文本输入": "cardigan",
            "意图说明": "搜索歌曲"
        }
    ],
    "同花顺": [
        {
            "App": "同花顺",
            "任务类型": "搜索",
            "文本输入": "002241.SZ",
            "意图说明": "搜索股票行情"
        }
    ],
    "雪球": [
        {
            "App": "雪球",
            "任务类型": "搜索",
            "文本输入": "002241.SZ",
            "意图说明": "搜索股票相关消息"
        }
    ],
    "喜马拉雅": [
        {
            "App": "喜马拉雅",
            "任务类型": "搜索",
            "文本输入": "红楼梦",
            "意图说明": "搜索有声读物"
        }
    ],
    "应用市场": [
        {
            "App": "应用市场",
            "任务类型": "搜索",
            "文本输入": "携程",
            "意图说明": "搜索app"
        }
    ],
    "ios地图": [
        {
            "App": "ios地图",
            "任务类型": "搜索",
            "文本输入": "肯德基",
            "意图说明": "找餐厅"
        },
        {
            "App": "ios地图",
            "任务类型": "搜索",
            "文本输入": "上海交通大学闵行校区",
            "意图说明": "规划出行路线"
        }
    ],
    "滴滴出行": [
        {
            "App": "滴滴出行",
            "任务类型": "搜索",
            "文本输入": "上海交通大学闵行校区",
            "意图说明": "搜索目的地"
        }
    ],
    "抖音": [
        {
            "App": "抖音",
            "任务类型": "搜索",
            "文本输入": "三三制战术",
            "意图说明": "搜索军事知识"
        },
        {
            "App": "抖音",
            "任务类型": "搜索",
            "文本输入": "背部训练计划",
            "意图说明": "搜索健身计划"
        },
        {
            "App": "抖音",
            "任务类型": "搜索",
            "文本输入": "布莱恩洛佩兹",
            "意图说明": "搜索人物"
        }
    ],
    "起点读书": [
        {
            "App": "起点读书",
            "任务类型": "搜索",
            "文本输入": "诡秘之主",
            "意图说明": "搜索小说"
        }
    ],
    "虎牙直播": [
        {
            "App": "虎牙直播",
            "任务类型": "搜索",
            "文本输入": "lol",
            "意图说明": "搜索直播"
        }
    ],
    "百度": [
        {
            "App": "百度",
            "任务类型": "搜索",
            "文本输入": "python list copy",
            "意图说明": "搜索直播"
        }
    ]
}

GPT_URL = 'http://220.249.18.254:31999/gpt/v1/completion'
APP_LABEL_DICT = {
    '新闻资讯': ['浏览器', '今日头条', '百度', '微博'],
    '聊天': ['微信'],
    '社交': ['微信', '抖音', '微博', '知乎'],
    '支付': ['微信', '支付宝'],
    '短视频': ['抖音'],
    '搜索': ['百度'],
    '地图': ['高德地图', '百度地图'],
    '知识问答': ['百度', '知乎'],
    '网页浏览': ['百度','浏览器'],
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
    '电影': ['爱奇艺','哔哩哔哩'],
    '电视剧': ['爱奇艺','哔哩哔哩'],
    '综艺': ['爱奇艺','哔哩哔哩'],
    '音乐播放': ['酷狗音乐', 'QQ音乐', '网易云音乐'],
    '在线音乐': ['酷狗音乐', 'QQ音乐', '网易云音乐']
}

count_intend = 0
count_success = 0
count_top1 = 0
count_top3 = 0

for app, intend_list in SAMPLE.items():
    for intend in intend_list:
        isAppInList = intend['App'] in APP
        if (isAppInList):
            count_intend += 1
            print(intend['App'], intend['文本输入'])
            predict_label = send_to_gpt(intend['文本输入'])
            predict_app = {}
            for label in predict_label:
                if label in APP_LABEL_DICT:
                    # predict_app.extend(APP_LABEL_DICT[label])
                    init_point = 5
                    for p_app in APP_LABEL_DICT[label]:
                        predict_app[p_app] = predict_app.get(
                            p_app, 0)+init_point
                        init_point -= 1

            # predict_app = set(predict_app)
            # if intend['App'] in predict_app:
            #     count_success+=1

            predict_all = get_top(predict_app, len(predict_app))
            predict_top1 = get_top(predict_app, 1)
            predict_top3 = get_top(predict_app, 3)

            if intend['App'] in predict_all:
                count_success += 1
            if intend['App'] in predict_top1:
                count_top1 += 1
            if intend['App'] in predict_top3:
                count_top3 += 1

            if not intend['App'] in predict_all:
                print("FAILED")

            print(predict_label)
            print(sorted(predict_app, key=lambda x: x[1], reverse=True))
            print("TOTAL:{}, SUCCESS:{}, ACC:{}, TOP1:{}, ACC:{}, TOP3:{}, ACC:{}".format(count_intend,
                  count_success, format(count_success/count_intend, '.2f'), count_top1, format(count_top1/count_intend, '.2f'), count_top3, format(count_top3/count_intend, '.2f')))
            print('\n')
