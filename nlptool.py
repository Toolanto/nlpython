# Developer Antonio Luca
# coding=utf-8

import nltk
import itertools
import math
import re
from csvHandler import *
from store import *

#Passando una regex  al costruttore si ha una tokenizzazione custom
class CustomTokenizer(nltk.RegexpTokenizer):
  def __init__(self,customRegex):
    nltk.RegexpTokenizer.__init__(self,customRegex,gaps=True)

class NLP():
  def __init__(self,pathDocument,nameCorpus):
    d = CSVHandler(pathDocument)
    self.corpusDB = StoreCorpus(nameCorpus) #è il corpus salvato nel db senza modifiche
    self.corpusDB.makeDB()
    self.corpusDB.storeDB(d)
    self.corpus = {} #il corpus salvato in memoria tokenizato

  def delete(self):
    self.corpusDB.deleteDB()

  def getCorpus(self):
    return self.corpus

  #regexTokenizer è la classe o la sottoclasse di RegexpTokenizer
  def tokenize(self,regexpTokenizer=nltk.WhitespaceTokenizer()):
    self.corpus = {idn:regexpTokenizer.tokenize(text) for idn,text in self.corpusDB.searchAll()}
    for key,doc in self.corpus.items():
      temp = [token.lower() for token in doc]
      self.corpus[key] = temp
  
  #rimozione delle stopword nel corpus in memoria
  def removeStop(self,listWord):
    self.corpus = {key : [word for word in self.corpus[key] if word not in listWord] for key in self.corpus.keys()} 
 
  def calculate_tf(self,term,text):pass
  def getDocumentsByToken(self,token):pass
  
  def calculate_idf(self,token):
    return math.log(float(len(self.corpus))/float((len(self.getDocumentsByToken(token))+1)))  
  def calculate_tfidf(self,token,document):
    return self.calculate_tf(token,document)*self.calculate_idf(token)
  

class StandardNLP(NLP):
  #il calcolo del tf è consentito solo su termini di un solo token
  #perché si conta nella lista quante volte il token è presente
  def calculate_tf(self,token,document):
    return document.count(token)
  def getDocumentsByToken(self,token):
    docsID = [key for key in self.corpus.keys() if token in self.corpus[key]] #tutti i documenti che hanno il token
    return [(idn,self.corpusDB.searchByIdentifier(idn)) for idn in docsID] #prelevo dal db i documenti senza modifiche
  #ngram è una sottoclasse di Ngram
  def findngram(self,document,ngram,threshold):
    return ngram.findgram(self.corpus[document],threshold)

class Ngram():
  def findgram(self,text,threshold):
    pass

class Bigram(Ngram):
  def findgram(self,text,threshold):
    bigram_measures = nltk.BigramAssocMeasures()
    bigrams = nltk.BigramCollocationFinder.from_words(text)
    return bigrams.nbest(bigram_measures.pmi,threshold)

 
class Trigram(Ngram):
  def findgram(self,text,threshold):
    trigram_measures = nltk.TrigramAssocMeasures()
    trigrams = nltk.TrigramCollocationFinder.from_words(text)
    return trigrams.nbest(trigram_measures.pmi,threshold)


if __name__=='__main__':


  snlp = StandardNLP("document.txt","corpus.db")
  snlp.tokenize()
  #print snlp.getCorpus()
  #nlp.removeStop(['casa','ciao'])   
  for key,doc in snlp.getDocumentsByToken('memoria'):
    print key,doc[0].encode('utf-8')
  
  print "tf: {0}".format(snlp.calculate_tf("memoria",snlp.getCorpus()['CAPITOLO VIII']))
  print "idf: {0}".format(snlp.calculate_idf("memoria")) 
  print "tf_idf: {0}".format(snlp.calculate_tfidf("memoria",snlp.getCorpus()['CAPITOLO VIII']))
  
  ngram = []
  for ngram in snlp.findngram('CAPITOLO VIII',Bigram(),10):
    gram = ""
    for n in ngram:
     gram += n.encode('utf-8')
     gram +=" "
    print gram
  snlp.delete()  
  
