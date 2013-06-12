# Developer Antonio Luca
# coding=utf-8

import sys
import getopt
from nlptool import * 

def main(argv):
  document = ''
  corpusDB = ''
 
  try:
    document = argv[0]	
  except:
    print "python <pathdocument> [namecorpus]"
    sys.exit(2)
  try:
    corpusDB = argv[1]
  except:
    corpusDB = "corpus.db"
  print "\n\n******* NLP programm *******\n"
  nlp = NLP(document,corpusDB) 
  print "\nTokenize: waiting for a monent...\n"
  regex = r'''\s+|\W+'''
  ct = CustomTokenizer(regex)
  nlp.tokenize(ct)
  response = raw_input("\nWould you remove some stopword ?\nReply (Y or N): ")
  if (response == 'y' or response == 'Y'):
    stopwords = raw_input("Insert the stopwords separate by comma: ")
    stopwords = stopwords.split(',')
    nlp.removeStop(stopwords)
  for key,doc in nlp.getCorpus().items():
    print key
    print doc
    try:
      raw_input ("Press enter to continue")
    except:
      continue    
  exit = True
  while (exit):
    try:
      n = int(input('''\nSelect menù:
             1) tf of a term
             2) Give documents by token
             3) tf-idf
             4) find ngram
             5) make vector tf-idf
             6) show document
             any value to exit
             Reply:  ''')) 
    except:
      nlp.delete()
      sys.exit()     
    if n == 1:
      term = raw_input("\nEnter term: ")
      print "\tidDoc\t\ttf"
      for key in nlp.getCorpus().keys():
        tf = nlp.calculate_tf(term,key)
        print "\t{0}\t\t{1}".format(key,tf)
    if n == 2:
      token = unicode(raw_input("\nEnter token: "))
      token = token.lower()
      documents = nlp.getDocumentsByToken(token)
      for doc in documents:
        print doc[0]
    if n == 3:
      try:
        document = raw_input("\nEnter document's id: ")
        template = "{0:20}|{1:20}|" 
        print template.format("TERM", "TF-IDF", ) 
        setTerm = {p for p in nlp.getCorpus()[document]}
        i = 0
        for term in setTerm:
          tfidf = nlp.calculate_tfidf(term,document)
          print template.format(term.encode('utf-8'),tfidf)
          i+=1
          try:
            if (i%40 == 0) : raw_input ("Press enter to continue")
          except:
            continue
      except KeyError:
        print "Nessun documento trovato"
    if n == 4:
      try:
        document = input("\nEnter deocument's id: ")
        print nlp.findngram(document,2,0.3)
      except KeyError:
        print "Nessun documento trovato"
    if n == 5:
      try:
        document = input("\nEnter deocument's id: ")
        print nlp.makevector(document)
      except KeyError:
        print "Nessun documento trovato"
    if n == 6:
      try:
        document = input("\nEnter deocument's id: ")
        print nlp.getCorpus()[document]
      except KeyError:
        print "Nessun documento trovato"      
    try:
      if n not in[1,2,3,4,5,6]:
        exit = False
    except:
      exit = False
  nlp.delete()


  


if __name__=='__main__':
  main(sys.argv[1:])
