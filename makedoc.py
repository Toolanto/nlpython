# coding=utf-8
from nltk.corpus import gutenberg

corpus = ""
i = 0
doc = gutenberg.raw['austen-emma.txt'].split("\n")
for raw in doc:
  corpus += '{0},\"{1}"\n'.format(i,raw)
  i+=1
f = open('doc.txt','w')
f.write(corpus)
f.close() 
