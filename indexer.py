import re, sys, os, keywords_extractor
import json, operator
from collections import OrderedDict

def lister(dir_name): #Lists all the files and folders in the current working directory
    filesList = []
    for root, dirs, files in os.walk(dir_name, topdown=False):
        for name in files:
            filesList.append(name)
        for name in dirs:
            lister(name)
    return filesList

def normalize(text):
        text = re.sub("[^A-Za-z_]", " ", text)
        text = re.sub(" +"," ",text)
        text = text.lower()
        return text

dir_name = input("Directory: ")
filesList = lister(os.getcwd()+"/"+dir_name)

index = {}
index["docslist"] = filesList
for eachFile in filesList:
    print(eachFile)
    f = open(dir_name+"/"+eachFile, encoding = "ISO-8859-1")
    text = f.read()
    f.close()
    text = normalize(text)
    words = text.split(" ")

    for i in range(len(words)):
        if words[i] not in index.keys():
            index[words[i]] = {}
        else:
            wordMap = index[words[i]]
            if eachFile not in wordMap.keys():
                # Positions not added for that document
                wordMap[eachFile] = []
            wordMap[eachFile].append(i)
            index[words[i]] = wordMap

    # extractor = keywords_extractor.Extractor(text)
    # keywords = extractor.rank_words()
    # print(keywords)
    # for j in range(len(keywords)):
    #     if keywords[j] not in index.keys():
    #         index[keywords[j]] = []
    #     if eachFile not in index[keywords[j]]:
    #         index[keywords[j]].append(eachFile)
    #     index[keywords[j]].sort()

# print(index)

indexFile = open(os.getcwd()+"/index.json", "w")
index = OrderedDict(sorted(index.items(), key=lambda t: t[0]))
indexFile.write(json.dumps(index))
indexFile.close()

