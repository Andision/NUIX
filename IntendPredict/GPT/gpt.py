import openai
import json

# ========== Config ==========

DEBUG_FALSE = -1
DEBUG_INFO = 0
DEBUG_VITAL = 10
DEBUG_LEVEL = DEBUG_VITAL
OPENAI_KEY = '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'
INTEND_SAMPLE_FILE = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/intend.json"
APP_LABELS_FILE = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/label.json"

# ========== Init ==========

# set OpenAI Key
openai.api_key = OPENAI_KEY

# Load JSON
with open(INTEND_SAMPLE_FILE, encoding='utf-8') as f:
    intendSamples = json.load(f)
with open(APP_LABELS_FILE, encoding='utf-8') as f:
    AppLabels = json.load(f)

# Get All App in Sample
AppList = []

for app, intendList in intendSamples.items():
    for intend in intendList:
        # print(app,intend)
        AppList.append(app)

AppList = set(AppList)

# Get App Label in label.json

LabelList = []

for app in AppLabels:
    for label in AppLabels[app]:
        LabelList.append(label)

LabelList = set(LabelList)


# ========== Function ==========

def PrintLog(*msgs, tag="", level=DEBUG_INFO):
    if level < DEBUG_LEVEL:
        return

    print("\n+++++ TAG:{} +++++".format(tag))
    for i in msgs:
        print(i)
    print("----- TAG:{} -----\n".format(tag))


def ChatGPTCompletionRaw(prompt: str, model: str = "gpt-3.5-turbo"):

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    PrintLog(completion)

    ret = completion.choices[0].message.content.strip()
    PrintLog(ret)
    return ret


def ChatGPTIntendApp(keyword: str):
    res = ChatGPTCompletionRaw(
        "我手机里的应用程序有{}，当我输入的关键词是“{}”时，我最有可能想使用的5个应用程序是什么。必须给出可能的应用程序，按照我可能使用的概率从高到低排序，应用程序之间用“|”分隔，只给出应用程序，不要出现我手机里没有的应用程序，不要任何解释和上下文。".format(AppList, keyword))
    PrintLog(res)

    ret = res.split("|")
    return ret


def ChatGPTIntendLabel(keyword: str):
    res = ChatGPTCompletionRaw(
        "我有一些对关键词分类的标签{}。关键词“{}”和哪些标签的关联度最大？给出相关的10个标签，按照可能性从高到低排序，只能出现我给出过的标签，标签之间用“|”分隔。只给出标签，不要任何解释和上下文。".format(LabelList, keyword))
    PrintLog(res)

    ret = res.split("|")
    return ret

def Label2App(labels:list):
    ret = {}
    for label in labels:
        for appName,labelList in AppLabels.items():
            if label in labelList:
                if label in labels[:3]:
                    ret[appName] = ret.get(appName,0) + 5
                
                elif label in labels[3:5]:
                    ret[appName] = ret.get(appName,0) + 3

                elif label in labels[5:]:
                    ret[appName] = ret.get(appName,0) + 1

    return ret

def GetTopKeyInDict(inputDict: dict, top: int = -1) -> dict:
    if top == -1:
        top = len(inputDict)
    ret = []
    for i in sorted(inputDict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if top == 0:
            break
        top -= 1
        ret.append(i)

    return {i[0]: i[1] for i in ret}





