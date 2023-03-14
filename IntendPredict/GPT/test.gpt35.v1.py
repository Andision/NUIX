import json

import gpt


intendSamplesFile = gpt.INTEND_SAMPLE_FILE
AppLabelsFile = gpt.APP_LABELS_FILE

gpt.PrintLog("Loading Json...")
with open(intendSamplesFile, encoding='utf-8') as f:
    intendSamples = json.load(f)
with open(AppLabelsFile, encoding='utf-8') as f:
    AppLabels = json.load(f)
gpt.PrintLog("JSON loaded!")

countIntend = 0
countSuccess = 0
countTop1 = 0
countTop5 = 0

for app, intendList in intendSamples.items():
    for intend in intendList:
        if intend['App'] in AppLabels and len(AppLabels[intend['App']]) > 0:

            print(intend['App'], intend['文本输入'])

            # predict app
            predictAppListAll = gpt.ChatGPTIntendApp(intend['文本输入'])

            # calculate accuracy
            countIntend += 1

            predictAppListTop5 = predictAppListAll[:5]
            predictAppListTop1 = predictAppListAll[:1]

            if intend['App'] in predictAppListTop5:
                countTop5 += 1
            if intend['App'] in predictAppListTop1:
                countTop1 += 1

            # print(predictAppDict)
            # print(sorted(predictAppDict.items(), key=lambda x: x[1], reverse=True))
            print("TOP5:{}, TOP1:{}".format(
                intend['App'] in predictAppListTop5, intend['App'] in predictAppListTop1))
            print(predictAppListTop5)
            print("TOTAL:{}, TOP5:{}, ACC:{:.2f}, TOP1:{}, ACC:{:.2f}\n".format(
                countIntend, countTop5, countTop5/countIntend, countTop1, countTop1/countIntend))
