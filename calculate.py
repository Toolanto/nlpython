# Developer Antonio Luca
# coding=utf-8


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
