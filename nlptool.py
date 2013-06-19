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
    self.corpus = {idn:regexpTokenizer.tokenize(text.lower()) for idn,text in self.corpusDB.searchAll()}
  
  #regexTokenizer è la classe o la sottoclasse di RegexpTokenizer
  def sentencetokenize(self,regexpTokenizer=nltk.WhitespaceTokenizer(), length=100):
    for idn,text in self.corpusDB.searchAll():      
      temp = [text[i:length+i] for i in range(0,len(text),length)]
      token = [] 
      for tb in temp:
         token += regexpTokenizer.tokenize(tb.lower())
      self.corpus[idn] = token
    self.corpus

  #rimozione delle stopword nel corpus in memoria
  def removeStop(self,listWord):
    self.corpus = {key : [word for word in self.corpus[key] if word.encode('utf-8') not in listWord] for key in self.corpus.keys()} 
  
  def removeStandard(self,language):
    self.corpus = {key : [word for word in self.corpus[key] if word.encode('utf-8') not in nltk.corpus.stopwords.words(language)] for key in self.corpus.keys()} 
 
  def calculate_idf(self,token):
    return math.log(float(len(self.corpus))/float((len(self.getDocumentsByToken(token))+1)))  
  def calculate_tfidf(self,token,idDoc):
    return self.calculate_tf(token,idDoc)*self.calculate_idf(token)

  #il calcolo del tf è consentito solo su termini di un solo token
  #perché si conta nella lista quante volte il token è presente
  def calculate_tf(self,token,idDoc):
    return self.corpus[idDoc].count(token)
  
  def getDocumentsByToken(self,token):
    docsID = [key for key in self.corpus.keys() if token in self.corpus[key]] #tutti i documenti che hanno il token
    return [(idn,self.corpusDB.searchByIdentifier(idn)) for idn in docsID] #prelevo dal db i documenti senza modifiche
  #ngram è una sottoclasse di Ngram
  def findngram(self,idDoc,ngram,threshold):
    return ngram.findgram(self.corpus[idDoc],threshold)
  def makeVector(self,idDoc):
    return {tok:self.calculate_tfidf(tok,idDoc) for tok in self.corpus[idDoc]}
      

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


class IndexNLP(NLP):
  #regexTokenizer è la classe o la sottoclasse di RegexpTokenizer
  def tokenize(self,regexpTokenizer=nltk.WhitespaceTokenizer()):
    NLP.tokenize(self,regexpTokenizer)
    setToken = set()
    for token in self.corpus.values():
      setToken.update(set(token))
    self.inverted_index = {}
    for token in setToken:
      for idn in self.corpus.keys():
        if token in self.corpus[idn]:
          if token in self.inverted_index:
            self.inverted_index[token].append(idn)
          else:
            self.inverted_index[token] = [idn]
  def calculate_idf(self,token):
    return math.log(float(len(self.corpus))/float((len(self.inverted_index[token])+1))) 
  #def getDocumentsByToken(self,token):
  #  return self.inverted_index[token]  
    
def lowerList(text):
  return [t.lower() for t in text]
 

if __name__=='__main__':
  snlp = NLP("document.txt","corpus.db")
  snlp.tokenize()
  #print snlp.getCorpus()
  #nlp.removeStop(['casa','ciao'])   
  #for key,doc in snlp.getDocumentsByToken('memoria'):
  #  print key,doc[0].encode('utf-8')
  
  print "tf: {0}".format(snlp.calculate_tf("memoria",'CAPITOLO VIII'))
  print "idf: {0}".format(snlp.calculate_idf("memoria")) 
  print "tf_idf: {0}".format(snlp.calculate_tfidf("memoria",'CAPITOLO VIII'))
  
  ngram = []
  for ngram in snlp.findngram('CAPITOLO VIII',Bigram(),10):
    gram = ""
    for n in ngram:
     gram += n.encode('utf-8')
     gram +=" "
    print gram

  print snlp.makeVector('CAPITOLO VIII')

  snlp.delete() 
  nlp = IndexNLP("document.txt","corpus.db") 
  nlp.tokenize()
  print nlp.getDocumentsByToken(unicode('parola'))
  print "tf_idf: {0}".format(nlp.calculate_tfidf("memoria",'CAPITOLO VIII'))
  nlp.delete()   
