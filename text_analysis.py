#!usr/bin/python3 

import requests
import bs4 as bs
from  bs4 import BeautifulSoup 
import webbrowser
import os 
import urllib.request  
import re
import heapq  
import nltk
from googlesearch import search

# Take the input from user about whatever the user wnats to ask
msg=input("type to search ")
wiki="best definition of "+msg

#storing all URLs in a list and then pick up the first url scrapped 
table=[]
for url in search( wiki, stop=1):
	table.append(url)

#[picking up the first url scrapped for the further nlp application]
scraped_data = urllib.request.urlopen(table[0])  

article = scraped_data.read()

#scrapping the page via Beautiful Soup
parsed_article = bs.BeautifulSoup(article,'lxml')

#gathering all the text in the link by grabbing the 'p' tags in the page
paragraphs = parsed_article.find_all('p')

#collecting all the text in an article form and storing that in another variable
article_text = ""

for p in paragraphs:  
    article_text += p.text

# Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
article_text = re.sub(r'\s+', ' ', article_text)  

# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  

#converting text to sentences 
sentence_list = nltk.sent_tokenize(article_text) 

#finding weighted frequency of occurrence 
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}  
for word in nltk.word_tokenize(formatted_article_text):  
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


# to find the weighted frequency, we can simply divide the number of occurances of all the words by the frequency of the most occurring word
maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():  
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


#Calculating Sentence Scores
sentence_scores = {}  
for sent in sentence_list:  
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]


#Getting the Summary
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)  
print(summary) 
