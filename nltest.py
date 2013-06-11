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
    print "python [pathdocument] <namecorpus>"
    sys.exit(2)
  try:
    corpusDB = argv[1]
  except:
    corpusDB = "corpus.db"
  print "\n\n******* NLP programm *******\n"
  nlp = NLP(document,corpusDB) 
  print "\nTokenize: waiting for a monent...\n"
  nlp.tokenize()
  response = raw_input("\nWould you remove some stopword ?\nReply (Y or N): ")
  if (response == 'y' or response == 'Y'):
    stopwords = raw_input("Insert the stopwords separate by comma: ")
    stopwords = stopwords.split(',')
    nlp.removeStop(stopwords)
  exit = True
  while (exit):
    n = int(input('''\nSelect menù:
             1) tf of a term
             2) Give documents by token
             3) tf-idf
             4) find ngram
             5) make vector tf-idf
             any value to exit
             Reply:  '''))      
    if n == 1:
      term = raw_input("\nEnter term: ")
      print "\tidDoc\t\ttf"
      for key in nlp.getCorpus().keys():
        tf = nlp.calculate_tf(term,nlp.getCorpus()[key])
        print "\t{0}\t\t{1}".format(key,tf)
    if n == 2:
      token = raw_input("\nEnter token: ")
      documents = nlp.getDocumentsByToken(token)
      print documents
    if n == 3:
      try:
        document = raw_input("\nEnter document's id: ")
        print "\tterm\ttf-idf"
        setTerm = {p for p in nlp.getCorpus()[document]}
        i = 0
        for term in setTerm:
          tfidf = nlp.calculate_tfidf(term,document)
          print "\t{0}\t{1}".format(term.encode('utf-8'),tfidf)
          i+=1
          try:
            if (i%80 == 0) : raw_input ("Press enter to continue")
          except:
            continue
      except KeyError:
        print "Nessun documento trovato"
    if n == 4:
      document = input("\nEnter deocument's id: ")
      print nlp.findngram(document,2,0.3)
    try:
      if n not in[1,2,3,4]:
        exit = False
    except:
      exit = False
  nlp.delete()

if __name__=='__main__':
  main(sys.argv[1:])
