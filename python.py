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
dups = []
def readDups():
    f = open("dedup.txt", "r")
    for line in f.readlines():
        dups.append(line)
    f.close()

def createFiles():
    # f = open("from.csv", "w")
    # f.close()

    # f = open("to.csv", "w")
    # f.close()

    # f = open("global_keyword.csv", "w")
    # f.close()

    # f = open("individual_keyword.csv", "w")
    # f.close()

    # f = open("sentinment.csv", "w")
    # f.close()

    # f = open("keyword1.csv", "w")
    # f.close()

    # f = open("keyword2.csv", "w")
    # f.close()

    # f = open("keyword3.csv", "w")
    # f.close()

    # f = open("intersect.csv", "w")
    # f.close()
    f = open("keyword_combine.csv", "w")
    f.close()
    f = open("keywords_flagged_emails.json", "w")
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

arr1 = ["special","purpose", "entity", "chewco", "whitewing", "ljm", "ljm1", "ljm2", "raptor", "transfer", "offshore", "losses", "accounting", "fix", "adjustment", "conceal", "hide", "cover", "up", "trouble","shit", "fuck", "destroy", "upset", "angry", "idiot", "wtf", "fire"]

masterLIST1 = []
def keywordList(data, emailID, From):
    data = [x.lower() for x in data]
    found = set(arr1).intersection(set(data)) 
    master = str(emailID)+","+str(From)
    if found:
        masterLIST1.append(str(emailID))
        master += ","+ str(len(found))
        for x in found:
            master += ","+str(x)
        keywordList1ARRAY.append(master)

masterLIST2 = []
def keywordList2(data, emailID, From):
    data = [x.lower() for x in data]
    found = set(arr2).intersection(set(data))
    master = str(emailID)
    if found:
        masterLIST2.append(str(emailID))
        for x in found:
            master += ","+str(x)
        master+=","+str(From)
        keywordList2ARRAY.append(master)

masterLIST3 = []
def keywordList3(data, emailID, From):
    data = [x.lower() for x in data]
    found = set(arr3).intersection(set(data))
    master = str(emailID)
    if found:
        masterLIST3.append(str(emailID))
        for x in found:
            master += ","+str(x)
        master+=","+str(From)
        keywordList3ARRAY.append(master)

def intersect():
    result = set(masterLIST1) & set(masterLIST2) & set(masterLIST3)
    return result

unique_sent_emails = []
def dedup():
    dups =0
    text = []
    my_dict = {}
    for filename in glob.glob(os.path.join(path, '*.json')):    
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            json_data = json.loads(data)
            name = json_data["headers"]["from"]
            date = json_data["text"]
            if date in text:
                dups+=1
                unique_sent_emails.append(filename)
            else:
                text.append(date)
    print(dups)

def main():   
    for filename in glob.glob(os.path.join(path, '*.json')):    
        if filename in dups:
            pass 
        else:
            with open(filename, encoding='utf-8', mode='r') as currentFile:
                data=currentFile.read().replace('\n', '')
                json_data = json.loads(data)
                # addFrom(json_data)
                # addTo(json_data)
                words= word_tokenize(json_data["text"])
                useful_words = [word  for word in words if word not in stopwords.words('English')]
                frequency = nltk.FreqDist(useful_words)
                # globalKeywords(frequency)
                name = json_data["headers"]["from"]
                # individualKeywords(frequency, name)
                text = json_data["text"]
                # sentiment_analysis(text, name)
                keywordList(frequency.keys(), filename, json_data["headers"]["from"])
                # keywordList2(frequency.keys(), filename, json_data["headers"]["from"])
                # keywordList3(frequency.keys(), filename, json_data["headers"]["from"])
    print("done with main")
    for x in masterLIST1:
        with open(x, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            json_data = json.loads(data)
            words= word_tokenize(json_data["text"])
            useful_words = [word  for word in words if word not in stopwords.words('English')]
            frequency = nltk.FreqDist(useful_words)
            name = json_data["headers"]["from"]
            individualKeywords(frequency, name)
    print("done with master list")
    for element in indiviualKeyword_dict:
        temp = dict(sorted(indiviualKeyword_dict[element].items(), key=lambda item: item[1], reverse=True))
        indiviualKeyword_dict[element] = temp
    print("done with dictionary")

# f = open("keyword2.csv", "a")
# for x in keywordList2ARRAY:
#     f.write(x+"\n")
# f.close()

# f = open("keyword3.csv", "a")
# for x in keywordList3ARRAY:
#     f.write(x+"\n")
# f.close()

# with open('from.csv', 'a', newline='') as f:
#     writer = csv.writer(f)
#     for row in from_dict.items():
#         writer.writerow(row)

# with open('to.csv', 'a', newline='') as f:
#     writer = csv.writer(f)
#     for row in to_dict.items():
#         writer.writerow(row)

# with open('global_keyword.csv', 'a', newline='') as f:
#     writer = csv.writer(f)
#     for row in global_dict.items():
#         writer.writerow(row)

# with open('individual_keyword.csv', 'a', newline='') as f:
#     writer = csv.writer(f)
#     for row in indiviualKeyword_dict.items():
#         writer.writerow(row)

# with open('sentinment.csv', 'a', newline='') as f:
#     writer = csv.writer(f)
#     for row in sentiment_Dict.items():
#         writer.writerow(row)

# with open('intersect.csv', 'a', newline='') as f:
#     result = intersect()
#     if result:
#         for row in result:
#             f.write(str(row)+"\n")


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
#Execution time in seconds: 28631.080872774124

# dedup from date + sender 
# remove priority 
# andrew fastow/jeff.skilling@enron.com hits on those emails

#keywords_flagged_emails
#keyword_combine

if __name__ == "__main__":
    createFiles()
    readDups()
    main()
    
    f = open("keyword_combine.csv", "a")
    for x in keywordList1ARRAY:
        f.write(x+"\n")
    f.close()

    with open('keywords_flagged_emails.json', 'a', newline='') as f:
        json.dump(indiviualKeyword_dict, f)