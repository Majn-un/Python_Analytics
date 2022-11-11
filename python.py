import json
import os
import glob
import pprint
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

startTime = time.time()

keywordList = []
counter = 0

my_Sender_dict = {}
my_Reciever_dict = {}
my_globalKeyword_dict = {}
my_indivialKeyword_dict = {}
my_sentiment_dict = {}

path = 'C:/Users/Mohammed Hager/Documents/Python_Analytics/subset'

def addSender(json_data):
    if 'from' in json_data['headers']:       
        if json_data['headers']['from'] in my_Sender_dict:
            my_Sender_dict[json_data['headers']['from']] +=1
        else:
            my_Sender_dict[json_data['headers']['from']] = 0

def addReciever(json_data):
    if 'to' in json_data['headers']:
        if ',' in json_data['headers']['to']:
            temp = json_data['headers']['to'].split(',')
            for email in temp:
                if email.strip() in my_Reciever_dict:
                    my_Reciever_dict[str(email.strip())] +=1
                else:
                    my_Reciever_dict[str(email.strip())] = 0
        else:
            if json_data['headers']['to'] in my_Reciever_dict:
                my_Reciever_dict[json_data['headers']['to']] +=1
            else:
                my_Reciever_dict[json_data['headers']['to']] = 0 

def globalKeywords(frequency):
    for index in frequency.most_common(100):
        if index[0] in my_globalKeyword_dict:
            my_globalKeyword_dict[index[0]] += index[1]
        else:
            my_globalKeyword_dict[index[0]] = index[1]

def individualKeywords(frequency, name):
    if name in my_indivialKeyword_dict:
        for index in frequency.most_common(100):
            if index[0] in my_indivialKeyword_dict[name]:
                my_indivialKeyword_dict[name][index[0]] += index[1]
            else:
                my_indivialKeyword_dict[name][index[0]] = index[1]
    else:
        my_indivialKeyword_dict[name] = {}
        for index in frequency.most_common(100):
            if index[0] in my_indivialKeyword_dict[name]:
                my_indivialKeyword_dict[name][index[0]] += index[1]
            else:
                my_indivialKeyword_dict[name][index[0]] = index[1]

def sentiment_analysis(text, name):
    parse = text.split("\n")
    sia = SentimentIntensityAnalyzer()
    for sentence in parse:
        sentiment_dict = sia.polarity_scores(sentence)
        if name in my_sentiment_dict:
            if sentiment_dict['pos'] > sentiment_dict['neg']:
                if "pos" in my_sentiment_dict[name]:
                    my_sentiment_dict[name]["pos"] += 1
            else:
                if "neg" in my_sentiment_dict[name]:
                    my_sentiment_dict[name]["neg"] += 1
        else:
            my_sentiment_dict[name] = {"pos":0,"neg":0}
    
    
    
for filename in glob.glob(os.path.join(path, '*.json')):     
    with open(filename, encoding='utf-8', mode='r') as currentFile:
        data=currentFile.read().replace('\n', '')
        json_data = json.loads(data)
        addSender(json_data)
        addReciever(json_data)
        words= word_tokenize(json_data["text"])
        useful_words = [word  for word in words if word not in stopwords.words('English')]
        frequency = nltk.FreqDist(useful_words)
        globalKeywords(frequency)
        name = json_data["headers"]["from"]
        individualKeywords(frequency, name)
        text = json_data["text"]
        sentiment_analysis(text, name)
        
        
with open('sender_result.json', 'w') as fp:
    json.dump(my_Sender_dict, fp)

with open('reciever_result.json', 'w') as fp:
    json.dump(my_Reciever_dict, fp)

with open('GlobalKeywords.json', 'w') as fp:
    json.dump(my_globalKeyword_dict, fp)

with open('IndividualKeywords.json', 'w') as fp:
    json.dump(my_indivialKeyword_dict, fp)

with open('Sentinment.json', 'w') as fp:
    json.dump(my_sentiment_dict, fp)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))