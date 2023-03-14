import json

import gpt

intendSamplesFile = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/intend.json"
AppLabelsFile     = "C:/Users/Andision/Documents/GitHub/NUIX/IntendPredict/config/label.json"

print("Loading Json...")
with open(intendSamplesFile, encoding='utf-8') as f:
    intendSamples = json.load(f)
with open(AppLabelsFile, encoding='utf-8') as f:
    AppLabels = json.load(f)
print("JSON loaded!")

APPS=[]

LabelList = []

for app in AppLabels:
    for label in AppLabels[app]:
        LabelList.append(label)

LabelList = set(LabelList)

print(LabelList)




