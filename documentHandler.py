# Developer Antonio Luca

import csv
from store import *

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
  store = StoreCorpus("corpus.db")
  store.makeDB()
  store.storeDB(d)
  print store.searchByIdentifier(1)
  print store.searchAll()	
