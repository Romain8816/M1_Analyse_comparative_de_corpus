import datetime as dt
from gensim.summarization.summarizer import summarize
import pickle

import os
directory=os.getcwd()

# Création d'un corpus
class Corpus():
    
    def __init__(self,name):
        self.name = name # Nom du corpus 
        self.collection = {} # Liste des instances de la classe Document 
        self.id2doc = {} # indices des documents
        self.ndoc = 0 # retourne le nombre de documents
        self.sources=[]
        
    # Ajout d'un document
    def add_doc(self, doc):
        self.collection[self.ndoc] = doc # Ajout du doc dans collection, self.ndoc vaut 0 au début
        self.id2doc[self.ndoc] = doc.get_title() # get title de la classe document 
        self.ndoc += 1
        
    
    # def all_clean_txt(self):
    #     return [self.collection[i].get_clean_text() for i in self.collection]

    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection

    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)
    
    def __repr__(self):
        return self.name


    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    def save(self,file):
            pickle.dump(self, open(file,"wb" ))
    
    def get_sources(self):
        return self.sources
    
    def add_source(self,source):
        self.sources.append(source)
        

class Document():
    
    # constructeurs
    def __init__(self, date, title, text, url):
        self.date = date
        self.title = title
        self.text = text
        self.url = url
        

    # getters   

    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
    
    def get_source(self):
        pass
        
    def get_text(self):
        return self.text
    

    def __str__(self):
        return "Document: " + self.title
    
    def __repr__(self):
        return self.title

    def sumup(self,ratio):
        try:
            auto_sum = summarize(self.text,ratio=ratio,split=True)
            out = " ".join(auto_sum)
        except:
            out =self.title            
        return out
    
        
class RedditDocument(Document):
    
    def __init__(self, date, title,text, url):        
        Document.__init__(self, date, title, text, url)
        self.source = "Reddit"

    def get_source(self):
        return self.source
    
    def __str__(self):
        #return(super().__str__(self) + " [" + self.num_comments + " commentaires]")
        return Document.__str__(self) + ", "+ self.source
    

class ArxivDocument(Document):
    
    def __init__(self, date, title, text, url):
        #datet = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        Document.__init__(self, date, title, text, url)
        self.source = "Arxiv"
    
    def get_source(self):
        return self.source

    def __str__(self):
        return Document.__str__(self) + ", "+ self.source
    
