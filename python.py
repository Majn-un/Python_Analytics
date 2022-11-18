import json
import os
import glob
import csv
import time
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

startTime = time.time()

keywordList = []
counter = 0

from_dict = {}
to_dict = {}
global_dict = {}
indiviualKeyword_dict = {}
sentiment_Dict = {}
keywordList1ARRAY = []
keywordList2ARRAY = []
keywordList3ARRAY = []
keywordINTERSECT = []

path = 'C:/Users/Mohammed Hager/Documents/Python_Analytics/dataset'

def createFiles():
    f = open("from.csv", "w")
    f.close()

    f = open("to.csv", "w")
    f.close()

    f = open("global_keyword.csv", "w")
    f.close()

    f = open("individual_keyword.csv", "w")
    f.close()

    f = open("sentinment.csv", "w")
    f.close()

    f = open("keyword1.csv", "w")
    f.close()

    f = open("keyword2.csv", "w")
    f.close()

    f = open("keyword3.csv", "w")
    f.close()

    f = open("intersect.csv", "w")
    f.close()

def addFrom(json_data):
    if 'from' in json_data['headers']:       
        if json_data['headers']['from'] in from_dict:
            from_dict[json_data['headers']['from']] +=1
        else:
            from_dict[json_data['headers']['from']] = 0

def addTo(json_data):
    if 'to' in json_data['headers']:
        if ',' in json_data['headers']['to']:
            temp = json_data['headers']['to'].split(',')
            for email in temp:
                if email.strip() in to_dict:
                    to_dict[str(email.strip())] +=1
                else:
                    to_dict[str(email.strip())] = 0
        else:
            if json_data['headers']['to'] in to_dict:
                to_dict[json_data['headers']['to']] +=1
            else:
                to_dict[json_data['headers']['to']] = 0 

def globalKeywords(frequency):
    for index in frequency.most_common(100):
        if index[0] in global_dict:
            global_dict[index[0]] += index[1]
        else:
            global_dict[index[0]] = index[1]

def individualKeywords(frequency, name):
    if name in indiviualKeyword_dict:
        for index in frequency.most_common(100):
            if index[0] in indiviualKeyword_dict[name]:
                indiviualKeyword_dict[name][index[0]] += index[1]
            else:
                indiviualKeyword_dict[name][index[0]] = index[1]
    else:
        indiviualKeyword_dict[name] = {}
        for index in frequency.most_common(100):
            if index[0] in indiviualKeyword_dict[name]:
                indiviualKeyword_dict[name][index[0]] += index[1]
            else:
                indiviualKeyword_dict[name][index[0]] = index[1]

def sentiment_analysis(text, name):
    parse = text.split("\n")
    sia = SentimentIntensityAnalyzer()
    for sentence in parse:
        sentiment_dict = sia.polarity_scores(sentence)
        if name in sentiment_Dict:
            if sentiment_dict['pos'] > sentiment_dict['neg']:
                if "pos" in sentiment_Dict[name]:
                    sentiment_Dict[name]["pos"] += 1
            else:
                if "neg" in sentiment_Dict[name]:
                    sentiment_Dict[name]["neg"] += 1
        else:
            sentiment_Dict[name] = {"pos":0,"neg":0}

arr1 = ["special purpose entity", "chewco", "whitewing", "ljm", "ljm1", "ljm2", "raptor", "transfer", "offshore", "losses"]
masterLIST1 = []
def keywordList1(data, emailID, priority, From):
    data = [x.lower() for x in data]
    found = set(arr1).intersection(set(data))
    master = str(emailID)
    if found:
        masterLIST1.append(str(emailID))
        for x in found:
            master += ","+str(x)
        master+=","+str(priority)+","+str(From)
        keywordList1ARRAY.append(master)

arr2 = ["accounting", "fix", "adjustment", "conceal", "hide", "cover up", "trouble"]
masterLIST2 = []
def keywordList2(data, emailID, priority, From):
    data = [x.lower() for x in data]
    found = set(arr2).intersection(set(data))
    master = str(emailID)
    if found:
        masterLIST2.append(str(emailID))
        for x in found:
            master += ","+str(x)
        master+=","+str(priority)+","+str(From)
        keywordList2ARRAY.append(master)

arr3 = ["shit", "fuck", "destroy", "upset", "angry", "idiot", "wtf", "fire"]
masterLIST3 = []
def keywordList3(data, emailID, priority, From):
    data = [x.lower() for x in data]
    found = set(arr3).intersection(set(data))
    master = str(emailID)
    if found:
        masterLIST3.append(str(emailID))
        for x in found:
            master += ","+str(x)
        master+=","+str(priority)+","+str(From)
        keywordList3ARRAY.append(master)

def intersect():
    result = set(masterLIST1) & set(masterLIST2) & set(masterLIST3)
    return result

for filename in glob.glob(os.path.join(path, '*.json')):    
    with open(filename, encoding='utf-8', mode='r') as currentFile:
        print(counter)
        counter+=1
        data=currentFile.read().replace('\n', '')
        json_data = json.loads(data)
        addFrom(json_data)
        addTo(json_data)
        words= word_tokenize(json_data["text"])
        useful_words = [word  for word in words if word not in stopwords.words('English')]
        frequency = nltk.FreqDist(useful_words)
        globalKeywords(frequency)
        name = json_data["headers"]["from"]
        individualKeywords(frequency, name)
        text = json_data["text"]
        sentiment_analysis(text, name)
        keywordList1(frequency.keys(), filename, json_data["priority"], json_data["headers"]["from"])
        keywordList2(frequency.keys(), filename, json_data["priority"], json_data["headers"]["from"])
        keywordList3(frequency.keys(), filename, json_data["priority"], json_data["headers"]["from"])

f = open("keyword1.csv", "a")
for x in keywordList1ARRAY:
    f.write(x+"\n")
f.close()

f = open("keyword2.csv", "a")
for x in keywordList2ARRAY:
    f.write(x+"\n")
f.close()

f = open("keyword3.csv", "a")
for x in keywordList3ARRAY:
    f.write(x+"\n")
f.close()

with open('from.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for row in from_dict.items():
        writer.writerow(row)

with open('to.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for row in to_dict.items():
        writer.writerow(row)

with open('global_keyword.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for row in global_dict.items():
        writer.writerow(row)

with open('individual_keyword.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for row in indiviualKeyword_dict.items():
        writer.writerow(row)

with open('sentinment.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    for row in sentiment_Dict.items():
        writer.writerow(row)

with open('intersect.csv', 'a', newline='') as f:
    result = intersect()
    if result:
        for row in result:
            f.write(str(row)+"\n")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))