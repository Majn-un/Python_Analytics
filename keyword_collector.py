import json
import os
import glob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('vader_lexicon')



keyword_emails = []


def dedup():
    path = 'C:/Users/Mohammed Hager/Documents/Python_Analytics/dataset'
    email_contents  = []
    unique_sent_emails = []
    for filename in glob.glob(os.path.join(path, '*.json')):    
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            data=currentFile.read().replace('\n', '')
            json_data = json.loads(data)
            date = json_data["text"].lower()
            if (date not in email_contents) and (len(date) <= 5000):
                unique_sent_emails.append(filename)
            else:
                email_contents.append(date)
    return unique_sent_emails

keyword_list = ["special","purpose", "entity", "chewco", "whitewing", "ljm", "ljm1", "ljm2", "raptor", "transfer", "offshore", "losses", "accounting", "fix", "adjustment", "conceal", "hide", "cover", "up", "trouble","shit", "fuck", "destroy", "upset", "angry", "idiot", "wtf", "fire"]

def keywordList(data, emailID, From):
    if "@enron.com" in From:
        data = [x.lower() for x in data]
        found = set(keyword_list).intersection(set(data))
        master = str(emailID)+","+str(From)
        if found:
            master += ","+ str(len(found))
            for x in found:
                master += "," + str(x)
            master.replace("\\","\\\\")
            keyword_emails.append(master)

def main(unique_sent_emails):   
    path = 'C:/Users/Mohammed Hager/Documents/Python_Analytics/dataset'
    for filename in glob.glob(os.path.join(path, '*.json')):    
        if filename in unique_sent_emails:
            with open(filename, encoding='utf-8', mode='r') as currentFile:
                data=currentFile.read().replace('\n', '')
                json_data = json.loads(data)
                words= word_tokenize(json_data["text"])
                useful_words = [word  for word in words if word not in stopwords.words('English')]
                frequency = nltk.FreqDist(useful_words)
                keywordList(frequency.keys(), filename, json_data["headers"]["from"])
                
    f = open("keyword_combine.csv", "w+")
    for x in keyword_emails:
        f.write(x+"\n")
    f.close()

if __name__ == "__main__":
    arr = dedup()
    main(arr)