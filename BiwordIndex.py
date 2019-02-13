import re, sys, os
import json, operator, Preprocessor
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
    processor = Preprocessor.Preprocessor()
    text = re.sub("[^A-Za-z_]", " ", text)
    text = re.sub(" +"," ",text)
    text = text.lower()
    print(text)
    return processor.lemmetize(text)

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

    for i in range(len(words) - 1):
        phrase = words[i] + " " + words[i + 1]
        if phrase not in index.keys():
            index[phrase] = []
        if eachFile not in index[phrase]:
            index[phrase].append(eachFile)
        index[phrase].sort()

indexFile = open(os.getcwd()+"/biword-index.json", "w")
index = OrderedDict(sorted(index.items(), key=lambda t: t[0]))
indexFile.write(json.dumps(index))
indexFile.close()

