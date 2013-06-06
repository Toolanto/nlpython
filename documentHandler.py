# Developer Antonio Luca

import csv

class DocumentHandler:
  def __init__(self,path,dialect=csv.Dialect.delimiter):
    self._path = path
    self._dialect = dialect  
  def __iter__(self):
    document_file = open(self._path,'rb')
    self._documents = csv.reader(document_file,self._dialect)
    return self
  def next(self):
    doc = self._documents.next()
    return doc  
  
if __name__=="__main__":
  d = DocumentHandler("document.txt")
  for doc in d:
    print doc
