# -*- coding: utf-8 -*-

from gensim.parsing.preprocessing import remove_stopwords
from classes import *
#from data_cleaning_libraries import *

import re
import praw
import requests
import math
from bs4 import BeautifulSoup
import datetime as dt
import urllib.request
import xmltodict   
import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def data_cleaning(txt):
    txt=re.sub('(\<.*?\>)|(\{.*?\}|(\\n))',' ',txt)
    txt=re.sub('\S*([\^%_&@#$,/\\\]|.com)\S*',' ',txt)
    txt=re.sub('-',' ',txt)
    txt=re.sub(r'(\b\d+\b)|\n',' ',txt)
    # Suppression des caractères non alphanumériques
    txt=remove_stopwords(txt)
    txt=re.sub('\W',' ',txt)
    #txt=re.sub('[“”"‘\,.!?;\|:®©\(\)\[\]\{\}]|((’|\')s?)',' ',txt)
    txt=re.sub(r'\b\w{1,2}\b', '', txt)
    txt=re.sub(' +', ' ',txt)
    return txt


################################## Création du corpus  ##################################




def get_reddit(theme):
    docs = []
    
    sub=""
# Identifiants reddit 
    reddit = praw.Reddit(client_id='p1TGayMUQ4F0Lg', client_secret='FoHT9V7DC1BGDtq319n4-2FF-NI', user_agent='Reddit WebScrapping')

    if (theme=="Coronavirus"):
        sub="Coronavirus"
    elif (theme=='Energie nucléaire'):
        sub="NuclearEnergy"
        
# Récupération des articles(au mieux 30 par theme)
    hot_posts = reddit.subreddit(sub).hot(limit=30)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}

# Pour chaque document : 
    for post in hot_posts:
        try:
            if "reddit" in post.url:
                continue
            else:
                url = post.url
                print(url)
                r= requests.get(url,headers=headers)
                soup = BeautifulSoup(r.content,"html.parser")
                data=[p.text for p in soup.find_all('p')]
                data = ' '.join(data)
                data = data_cleaning(data.lower())
                if data !='':
                    datet = dt.datetime.fromtimestamp(post.created)
                    docs.append(RedditDocument(datet,post.title,data,url))

        except:
            print('***FAILED TO DOWNLOAD***')
            print(post.url)
            continue
        
    return docs 


def get_arxiv(theme):
    
    doc_list=[]
    
    if (theme=="Coronavirus"):
        url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
    
    elif (theme=="Energie nucléaire"):
        url = 'http://export.arxiv.org/api/query?search_query=all:nuclear+energy&start=0&max_results=100'
       
    #http://export.arxiv.org/api/query?search_query=ti:"electron thermal conductivity"&sortBy=lastUpdatedDate&sortOrder=ascending
    data =  urllib.request.urlopen(url).read().decode()
    docs = xmltodict.parse(data)['feed']['entry']
    for i in docs: # docs est une liste de "dictionnaires ordonnés"
        url_doc = i['id']
        datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
        title = i['title']
        txt = title+ ". " + i['summary']
        txt = txt.replace('\n',' ')
        txt = data_cleaning(txt.lower())
        doc_list.append(ArxivDocument(datet,title,txt,i['id']))
    return doc_list


def compare(c1,c2):
    txt_corpus=[]
    txt=[]
    for i in c1:
        txt.append(i.get_text())
    txt = ' '.join(txt)
    txt_corpus.append(txt)
    
    txt=[]
    for i in c2:
        txt.append(i.get_text())
    txt = ' '.join(txt)
    txt_corpus.append(txt)
    
    
    return txt_corpus

#https://stackoverflow.com/questions/35596128/how-to-generate-a-word-frequency-histogram-where-bars-are-ordered-according-to
def bar_plot(lst):
    counts = Counter(lst)
    labels, values = zip(*counts.items())
    indSort = np.argsort(values)[::-1]
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    indexes = np.arange(len(labels))
    bar_width = 0.35
    plt.bar(indexes[0:15], values[0:15])
    plt.xticks(indexes[0:15] + bar_width, labels[0:15],rotation='vertical')
    plt.show()
    fig.canvas.draw()


#creation de la matrice tfidf, par le biais d'un dictionnaire TF et un dictionnaire IDF
def get_tfidf(liste_textes):
    Split_List=list()
    Dict_Word_List=list()
    nb_art=len(liste_textes)
    Dict_TF=list()
    Dict_IDF={}
    Dict_TFIDF=list()
    for i in range(0,nb_art):
        #print(i)
        Split_List.append(liste_textes[i].split(" "))
    
    for i in range(0,nb_art):
        Dict_Word_List.append(dict.fromkeys(Split_List[i],0))
    
    for i in range(0,nb_art):
        for j in Split_List[i]:
            #print(j)
            Dict_Word_List[i][j]+=1
    
    #Calcul de Tf: tf(mot)=nb de repetition du mot dans un article/ nb total de mot dans ce même article
    for i in range(0,nb_art):
        temp={}
        for j,k in Dict_Word_List[i].items():
            #print(j,k)
            temp[j]=k/len(Split_List[i])
        Dict_TF.append(temp)
        
    #Calcul IDF(mot)=log(nb d'article/nb d'article avec le mot concerné))   
    #Dans un premier temps on fait un dictionnaire qui va réunir tous les mots de tous les articles
    for i in range(0,nb_art):
        for j,k in Dict_Word_List[i].items():
            Dict_IDF[j]=0
    
    #On procède au comptage du nb avec le mot concerné
    for i in range(0,nb_art):
        for j,k in Dict_Word_List[i].items():
            if k>0:
                Dict_IDF[j]+=1
    
    for j,k in Dict_IDF.items():
        Dict_IDF[j]= math.log(nb_art/+k)
    
    for i in range(nb_art):
        temp={}
        for j,k in Dict_TF[i].items():
            temp[j]=k*Dict_IDF[j]
            #Dict_TFIDF[i].append(dict.fromkeys(j,k*Dict_IDF[j]))
            #Dict_TFIDF[j]=k*Dict_IDF[j]
        Dict_TFIDF.append(temp)
    
    tfidf_p=pd.DataFrame(Dict_TFIDF)
    tfidf_p=tfidf_p.fillna(0)
    tfidf_p=tfidf_p.sort_index(axis=1)  
    all_tfidf=list()
    all_tfidf.append(Dict_TF)
    all_tfidf.append(Dict_TFIDF)
    all_tfidf.append(tfidf_p)
    
    return all_tfidf
    #retourne 3 élements(le dictionnaire TF comprenant la frequence des mots les plus utilisé pour tous les documents, 
    #le dictionnaire TFIDF qui contient le score de chaque mot pour chaque document, ainsi que la matrice TFIDF crée à partir du dictionnaire TFIDF)
