# Developer Antonio Luca
# coding=utf-8

import nltk
import itertools
import math
from documentHandler import *
from store import *


class NLP():
  def __init__(self,pathDocument,nameCorpus):
    d = DocumentHandler(pathDocument)
    self.corpusDB = StoreCorpus(nameCorpus) #è il corpus salvato nel db senza modifiche
    self.corpusDB.makeDB()
    self.corpusDB.storeDB(d)
    self.corpus = {} #il corpus salvato in memoria a cui si possono apportare delle modifiche
  def delete(self):
    self.corpusDB.deleteDB()
  def getCorpus(self):
    return self.corpus
  #regexTokenizer è la classe o la sottoclasse di RegexpTokenizer
  def tokenize(self,regexpTokenizer=nltk.WhitespaceTokenizer()):
    self.corpus = {idn:regexpTokenizer.tokenize(text) for idn,text in self.corpusDB.searchAll()}
  #rimozione delle stopword nel corpus in memoria
  def removeStop(self,listWord):
    self.corpus = {key : [word for word in self.corpus[key] if word not in listWord] for key in self.corpus.keys()} 
  def getDocumentsByToken(self,token):
    docsID = [key for key in self.corpus.keys() if token in self.corpus[key]] #tutti i documenti che hanno il token
    return [(idn,self.corpusDB.searchByIdentifier(idn)) for idn in docsID] #prelevo dal db i documenti senza modifiche
  #document è la lista di token di un documento
  def calculate_tf(self,token,document):
    return document.count(token)
  def calculate_idf(self,token):
    return math.log(float(len(self.corpus))/float((len(self.getDocumentsByToken(token))+1)))
  def calculate_tfidf(self,token,document):
    return self.calculate_tf(token,document)*self.calculate_idf(token)
  #ngram di tipo Ngram
  #def transformngram(self,ngram):
  #  self.corpusngram {key : [ngram.findgram(value)] for key,value in self.corpus}    
      
        



class Ngram():
  def findgram(self,text):
    pass

class Bigram(Ngram):
  def __init__(self):
    self._ngram = 2
  #text = ['a',.]
  def findgram(self,text):
    return nltk.util.ngrams(text,self._ngram)

class Trigramm(Ngram):
  def __init__(self):
    self._ngram = 3
  #text = ['a',.]
  def findgram(self,text):
    return nltk.util.ngrams(text,self._ngram)
             
    
#Passando una regex  al costruttore si ha una tokenizzazione custom
class CustomTokenizer(nltk.RegexpTokenizer):
  def __init__(self,customRegex):
    nltk.RegexpTokenizer.__init__(self,customRegex,gaps=True)
    
  
  
 
if __name__=='__main__':
  nlp = NLP("document.txt","corpus.db")
  nlp.tokenize()
  print nlp.getCorpus()
  nlp.removeStop(['casa','ciao'])
  print nlp.getCorpus()     
  print nlp.getDocumentsByToken("sono")
  print "tf: {0}, idf: {1}, tf-idf di sono nel documento 0: {2}".format(nlp.calculate_tf("sono",nlp.getCorpus()[0]),nlp.calculate_idf("sono"),nlp.calculate_tfidf("sono",nlp.getCorpus()[0]))
  print nlp.transformngram(Bigram())
  
