# Developer Antonio Luca

import nltk
import itertools
from documentHandler import *
from store import *


class NLP():
  def __init__(self,pathDocument,nameCorpus):
    d = DocumentHandler(pathDocument)
    self.corpusDB = StoreCorpus(nameCorpus) #è il corpus salvato nel db senza modifiche
    self.corpusDB.makeDB()
    self.corpusDB.storeDB(d)
    self.corpus = [] #il corpus salvato in memoria a cui si possono apportare delle modifiche
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
  
