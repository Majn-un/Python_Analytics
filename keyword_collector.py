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
arr1 = ["special","purpose", "entity", "chewco", "whitewing", "ljm", "ljm1", "ljm2", "raptor", "transfer", "offshore", "losses", "accounting", "fix", "adjustment", "conceal", "hide", "cover", "up", "trouble","shit", "fuck", "destroy", "upset", "angry", "idiot", "wtf", "fire"]

path = 'C:/Users/Mohammed Hager/Documents/Python_Analytics/dataset'
dups = []
def readDups():
    f = open("dedup.txt", "r")
    for line in f.readlines():
        dups.append(line)
    f.close()
masterLIST1 = []
def keywordList(data, emailID, From, count, found_int):
    if "@enron.com" in From:
        data = [x.lower() for x in data]
        found = set(arr1).intersection(set(data))
        master = str(emailID)+","+str(From)
        if found:
            found_int += 1
            print(str(found_int)+"/"+str(count))
            masterLIST1.append(str(emailID))
            master += ","+ str(len(found))
            for x in found:
                master += ","+str(x)
            master.replace("\\","\\\\")
            keywordList1ARRAY.append(master)
    return found_int

def main():   
    count = 0 
    found = 0 
    for filename in glob.glob(os.path.join(path, '*.json')):    
        if filename in dups:
            pass 
        else:
            with open(filename, encoding='utf-8', mode='r') as currentFile:
                count+=1
                data=currentFile.read().replace('\n', '')
                json_data = json.loads(data)
                words= word_tokenize(json_data["text"])
                useful_words = [word  for word in words if word not in stopwords.words('English')]
                frequency = nltk.FreqDist(useful_words)
                found = keywordList(frequency.keys(), filename, json_data["headers"]["from"], count, found)
    print("done with main")

if __name__ == "__main__":
    readDups()
    main()
    
    f = open("keyword_combine.csv", "a")
    for x in keywordList1ARRAY:
        f.write(x+"\n")
    f.close()