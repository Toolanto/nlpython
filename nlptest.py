# Developer Antonio Luca
# coding=utf-8

import sys
import getopt
from nlptool import * 

def main(argv):
  document = ''
  corpusDB = ''
  language = {'i':"italian",'e':"english"}
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
  print "\nTokenizing: waiting for a monent...\n"
  nlp = NLP(document,corpusDB) 
  regex = r'''\s+|\W+'''
  ct = CustomTokenizer(regex)
  nlp.tokenize(ct)
  response = raw_input("\nWould you remove some stopword ?\nEnter (Y or N): ")
  if (response == 'y' or response == 'Y'):
    response = "c"
    response = raw_input("Custom remove (c)\nStandard remove(s)\nEnter: ")
    if response == 's' or response == 'S': 
      response = "i"
      response = raw_input("Select language, insert:\ni) for italian language\ne)for english language\nEnter: ")
      try:
        nlp.removeStandard(language[response])
      except:
        nlp.removeStandard(language['i'])
    else:
      stopwords = raw_input("Insert the stopwords separate by comma: ")
      stopwords = stopwords.split(',')
      nlp.removeStop(stopwords) 
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
             Enter:  ''')) 
    except:
      nlp.delete()
      sys.exit()     
    if n == 1:
      term = raw_input("\nEnter term: ")
      template = "{0:20}|{1:20}|"
      print template.format("ID DOC", "TF", ) 
      for key in nlp.getCorpus().keys():
        tf = nlp.calculate_tf(term,key)
        print template.format(key,tf)
    if n == 2:
      token = unicode(raw_input("\nEnter token: "))
      token = token.lower()
      documents = nlp.getDocumentsByToken(token)
      for doc in documents:
        print doc[0]
    if n == 3:
      try:
        print 'ID DOCUMENTI:'+','.join(nlp.getCorpus().keys())
        document = raw_input("\nEnter document's id: ")
        token = raw_input("Enter token: ")
        template = "{0:20}|{1:20}|" 
        print template.format("TERM", "TF-IDF", ) 
        tfidf = nlp.calculate_tfidf(token,document)
        print template.format(token,tfidf)
      except KeyError:
        print "No documents found"
    if n == 4:
      try:
        print 'ID DOCUMENTI:'+','.join(nlp.getCorpus().keys())
        document = raw_input("\nEnter deocument's id: ")
        template = "{0:40}|{1:40}|" 
        print template.format("BIGRAM", "TRIGRAM", ) 
        step = 10
        bigram = nlp.findngram(document,Bigram(),step)
        trigram = nlp.findngram(document,Trigram(),step)
        for i in range(step):
          print template.format(' '.join(bigram[i]).encode('utf-8'),' '.join(trigram[i]).encode('utf-8'))
      except KeyError:
        print "No documents found"
    if n == 5:
      try:
        print 'ID DOCUMENTI:'+','.join(nlp.getCorpus().keys())
        document = raw_input("\nEnter deocument's id: ")
        template = "{0:20}|{1:20}|" 
        print template.format("TERM", "TF-IDF", ) 
        i = 0        
        for token,tfidf in nlp.makeVector(document).items():
          print template.format(token.encode('utf-8'),tfidf)
          i+=1
          try:
            if (i%40 == 0) : raw_input ("Press enter to continue")
          except:
            continue
      except KeyError:
        print "No documents found"
    if n == 6:
      try:
        print 'ID DOCUMENTI:'+','.join(nlp.getCorpus().keys())
        document = raw_input("\nEnter deocument's id: ")
        print nlp.getCorpus()[document]
      except KeyError:
        print "No documents found"      
    try:
      if n not in[1,2,3,4,5,6]:
        exit = False
    except:
      exit = False
  nlp.delete()


  


if __name__=='__main__':
  main(sys.argv[1:])
