from jsonConvertXML import json2xml
import os

jsonDir = "E:/Duke/DIBBS/crawl/new_version/Accuracy-check/json_merged"
outputDir = "./xml"
for file in os.listdir(jsonDir):
    if ((len(file) > 4) and (file[-5:] == '.json')):
        print(jsonDir + "/" + file)
        json2xml(jsonDir + "/" + file, outputDir)

for file in os.listdir(outputDir):
    pre, ext = os.path.splitext(file)
    if (ext != '.xml'):
        os.rename(outputDir + "/" + file, outputDir + "/" + pre + ".xml")
    while(pre[-4:] == '.xml'):
        pre = pre[:-4]
        os.rename(outputDir + "/" + file, outputDir + "/" + pre + ".xml")
        
