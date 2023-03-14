from gensim.models import KeyedVectors
import json

SIMILARITY_THRESHOLD = 0.4


def GetTopKeyInDict(d: dict, top: int = -1):
    if top == -1:
        top = len(d)
    ret = []
    for i in sorted(d.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if top == 0:
            break
        top -= 1
        ret.append(i)

    return {i[0]: i[1] for i in ret}
    # return [i[0] for i in ret]


intendSamplesFile = "C:/Users/Andision/Downloads/embedding/intend.json"
AppLabelsFile = "C:/Users/Andision/Downloads/embedding/label.json"

print("Loading Json...")
with open(intendSamplesFile, encoding='utf-8') as f:
    intendSamples = json.load(f)
with open(AppLabelsFile, encoding='utf-8') as f:
    AppLabels = json.load(f)
print("JSON loaded!")

countIntend = 0
countSuccess = 0
countTop1 = 0
countTop5 = 0
print("Loading Word2Vec...")
word2VectorFile = 'C:/Users/Andision/Downloads/embedding/tencent-ailab-embedding-zh-d200-v0.2.0-s.txt'
# word2VectorFile = 'C:/Users/Andision/Downloads/embedding/tencent-ailab-embedding-zh-d200-v0.2.0.txt'
word2Vector = KeyedVectors.load_word2vec_format(
    word2VectorFile, binary=False)
print("Word2Vec loaded!")

print('\n')

for app, intendList in intendSamples.items():
    for intend in intendList:
        if intend['App'] in AppLabels and len(AppLabels[intend['App']]) > 0:

            print(intend['App'], intend['文本输入'])

            # predict app
            predictAppDict = {}
            for appInDict in AppLabels:
                if len(AppLabels[appInDict]) == 0:
                    continue
                maxSimlilarity = -1
                for label in AppLabels[appInDict]:
                    try:
                        similarity = word2Vector.similarity(
                            label, intend['文本输入'])
                        maxSimlilarity = max(maxSimlilarity, similarity)
                    except:
                        similarity = -1

                predictAppDict[appInDict] = maxSimlilarity
                # if similarity > SIMILARITY_THRESHOLD:
                #     predictAppDict[appInDict] = maxSimlilarity

            # calculate accuracy
            if len(predictAppDict) > 0 and maxSimlilarity != -1:
                countIntend += 1

                predictAppListAll = GetTopKeyInDict(predictAppDict)
                predictAppListTop5 = GetTopKeyInDict(predictAppDict, 5)
                predictAppListTop1 = GetTopKeyInDict(predictAppDict, 1)

                if intend['App'] in predictAppListAll:
                    countSuccess += 1
                if intend['App'] in predictAppListTop5:
                    countTop5 += 1
                if intend['App'] in predictAppListTop1:
                    countTop1 += 1

                # print(predictAppDict)
                # print(sorted(predictAppDict.items(), key=lambda x: x[1], reverse=True))
                print("SUCCESS:{}, TOP5:{}, TOP1:{}".format(
                    intend['App'] in predictAppListAll,intend['App'] in predictAppListTop5, intend['App'] in predictAppListTop1))
                print(predictAppListTop5)
                print("TOTAL:{}, SUCCESS:{}, ACC:{:.2f}, TOP5:{}, ACC:{:.2f}, TOP1:{}, ACC:{:.2f}".format(
                    countIntend, countSuccess, countSuccess/countIntend, countTop5, countTop5/countIntend, countTop1, countTop1/countIntend))
            else:
                print("NO KEYWORD")

            print('\n')
