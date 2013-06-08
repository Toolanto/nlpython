# Developer Antonio Luca
# coding=utf-8

from nlptool import * 
  
print "\n\n******* NLP programm *******\n"
documents = raw_input ("Give corpus's path: ")
nlp = NLP(documents,"corpus.db")
print "\nTokenize: waiting for a monent...\n"
nlp.tokenize()
print "Corpus:\n{0}".format(nlp.getCorpus())
response = raw_input("\nWould you remove some stopword ?\nReply (Y or N): ")
if (response == 'y' or response == 'Y'):
  stopwords = raw_input("Insert the stopwords separate by comma: ")
  stopwords = stopwords.split(',')
  nlp.removeStop(stopwords)
  print "New corpus:\n{0}".format(nlp.getCorpus())
exit = True
while (exit):
  n = int(input('''\nSelect menù:
           1) tf of a term
           2) Give documents by token
           3) tf-idf
           4) find ngram
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
    document = input("\nEnter document's id: ")
    print "\tterm\t\ttf-idf"
    for term in nlp.getCorpus()[document]:
      tfidf = nlp.calculate_tfidf(term,nlp.getCorpus()[document])
      print "\t{0}\t\t{1}".format(term,tfidf)
  if n == 4:
    document = input("\nEnter deocument's id: ")
    print nlp.findngram(document,2,0.3)
  if n not in[1,2,3,4]:
    exit = False
nlp.delete()

