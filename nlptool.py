# Developer Antonio Luca
# coding=utf-8

import nltk
import itertools
import math
import re
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
    docsID = [key for key in self.corpus.keys() if self.calculate_tf(token,self.corpus[key])>0] #tutti i documenti che hanno il token
    return [(idn,self.corpusDB.searchByIdentifier(idn)) for idn in docsID] #prelevo dal db i documenti senza modifiche
  
  #calcola il numero di occorenze di un termine in un documento, il termine può essere composto
  def calculate_tf(self,term,text):
    #un token può essere anche un ngramma perciò ogni documento viene convertito in stringa e si fa
    #il match per vedere quante volte compare il token all'interno del documento
    document_str = ' '.join(text)
    pattern = r"(^{0}| {0})".format(term) #termine che puo trovarsi all'inizio del documento o al centro ma non può
                                          #essere una parte di un altro termine
    return len(re.findall(pattern,document_str))   
   
  #def getDocumentsByToken_token(self,token):
  #  docsID = [key for key in self.corpus.keys() if token in self.corpus[key]] #tutti i documenti che hanno il token
  #  return [(idn,self.corpusDB.searchByIdentifier(idn)) for idn in docsID] #prelevo dal db i documenti senza modifiche

  #def calculate_tf_token(self,token,document):
  #  return document.count(token)
  
  def calculate_idf(self,token):
    return math.log(float(len(self.corpus))/float((len(self.getDocumentsByToken(token))+1)))
  
  def calculate_tfidf(self,token,document):
    return self.calculate_tf(token,document)*self.calculate_idf(token)
  
  def findngram(self,document,ngram,threshold):
    allgram = [[n for n in gram] for gram in nltk.util.ngrams(self.corpus[document],ngram)]
    return [gram for gram in allgram if self.calculate_tfidf(' '.join(gram),self.corpus[document]) > threshold]
    
#Passando una regex  al costruttore si ha una tokenizzazione custom
class CustomTokenizer(nltk.RegexpTokenizer):
  def __init__(self,customRegex):
    nltk.RegexpTokenizer.__init__(self,customRegex,gaps=True)
        
'''
class Ngram():
  def findgram(self,text,number):
    pass

class Bigram(Ngram):
  #text = ['a',.]
  def findgram(self,text):
    #bigram_measures = nltk.BigramAssocMeasures()
    #bigrams = nltk.BigramCollocationFinder.from_words(text)
    #return bigrams.nbest(bigram_measures.pmi,10)
    return nltk.util.ngrams(text,2)

class Trigramm(Ngram):
  #text = ['a',.]
  def findgram(self,text):
    return nltk.util.ngrams(text,3)
'''             
 
if __name__=='__main__':
  nlp = NLP("document.txt","corpus.db")
  nlp.tokenize()
  print nlp.getCorpus()
  #nlp.removeStop(['casa','ciao'])
  print nlp.getCorpus()     
  print nlp.getDocumentsByToken("sono a casa")
  print "tf: {0}".format(nlp.calculate_tf("sono a",nlp.getCorpus()[0]))
  print "idf: {0}".format(nlp.calculate_idf("sono a")) 
  print "tf_idf: {0}".format(nlp.calculate_tfidf("sono a",nlp.getCorpus()[0]))
  print nlp.findngram(0,2,0.3)
  
