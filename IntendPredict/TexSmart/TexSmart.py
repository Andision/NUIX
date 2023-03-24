import json
import requests

TEX_SMART_URL = "https://texsmart.qq.com/api"

# obj = {"str": "张老师"}
# req_str = json.dumps(obj).encode()

# url = "https://texsmart.qq.com/api"
# r = requests.post(url, data=req_str)
# r.encoding = "utf-8"
# # print(r.text)
# print(json.loads(r.text))


LOCAL_FILE = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/local.json"
INTEND_SAMPLE_FILE = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/intend.json"
APP_LABELS_FILE = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/label.json"

INTEND_SAMPLE_TEST_FILE = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/sample.GPT.json"
TEXSMART_LABELS_FILE = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/label.texsmart.json"
# ========== Init ==========

# Load JSON
with open(INTEND_SAMPLE_FILE, encoding='utf-8') as f:
    intendSamples = json.load(f)
with open(APP_LABELS_FILE, encoding='utf-8') as f:
    AppLabels = json.load(f)
with open(LOCAL_FILE, encoding='utf-8') as f:
    LocalConfig = json.load(f)
with open(INTEND_SAMPLE_TEST_FILE, encoding='utf-8') as f:
    intendSamplesTest = json.load(f)
with open(TEXSMART_LABELS_FILE, encoding='utf-8') as f:
    texSmartLabel = json.load(f)


def GetTexSmartRaw(keyword: str):
    requestsObject = {"str": keyword}
    requestStr = json.dumps(requestsObject).encode()
    requestRaw = requests.post(TEX_SMART_URL, data=requestStr)
    requestRaw.encoding = "utf-8"
    requestJson = json.loads(requestRaw.text)
    # print(requestJson)
    return requestJson


def GetTexSmartEntityList(keyword: str):
    requestJson = GetTexSmartRaw(keyword)
    requestEntityList = requestJson['entity_list']
    # print(requestEntityList)

    return requestEntityList


# texSmartLabel = {}


# for app, intendList in intendSamples.items():
#     for intend in intendList:

#         # print(intend['App'], intend['文本输入'])
#         texSmartEntityList = GetTexSmartEntityList(intend['文本输入'])
#         texSmartEntitiesName = [entityInKeyword['type']['name']
#                                 for entityInKeyword in texSmartEntityList]
#         texSmartEntitiesChinese = [entityInKeyword['type']['i18n']
#                                    for entityInKeyword in texSmartEntityList]

#         dictPrint = {
#             'app': intend['App'],
#             'input': intend['文本输入'],
#             'texsmart': texSmartEntitiesName,
#             'textsmart_chinese': texSmartEntitiesChinese
#         }
#         print(dictPrint)

#         texSmartLabel[intend['App']] = list(set(list(texSmartLabel.get(
#             intend['App'], [])) + texSmartEntitiesName))


# print(texSmartLabel)

for app, intendList in intendSamples.items():
    for intend in intendList:
        print(intend['App'], intend['文本输入'])
        # print(sample['App'], sample['关键词'])
        predictApp = {}
        entityList = GetTexSmartEntityList(intend['文本输入'])
        tagList = [entityInKeyword['type']['name']
                for entityInKeyword in entityList]

        for texSmartApp, texSmartAppLabels in texSmartLabel.items():
            for tag in tagList:
                if tag in texSmartAppLabels:
                    predictApp[texSmartApp] = predictApp.get(texSmartApp, 0)+1

        print(predictApp)
