# Developer Antonio Luca

import csv
import sqlite3

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
  

class StoreCorpus:        
  def __init__(self,namedb):
    self._namedb = namedb
  def makeDB(self):
    conn = sqlite3.connect(self._namedb)
    TABLE = "CREATE TABLE corpus (id number, document text)"
    conn.execute(TABLE)
  def storeDB(self, documentHandler):
    conn = sqlite3.connect(self._namedb)
    c = conn.cursor()
    for document in documentHandler:
      ident = document[0]
      print ident
      text = document[1]
      print text
      QUERY = "INSERT INTO corpus VALUES ({0},\'{1}\')".format(ident,text)
      c.execute(QUERY)
      conn.commit()
  def deleteDB(self):
    conn = sqlite3.connect(self._namedb)
    QUERY = "DROP TABLE corpus"
    c = conn.cursor()
    c.execute(QUERY)
    
  
if __name__=="__main__":
  d = DocumentHandler("document.txt")
  store = StoreCorpus("corpus.db")
  store.makeDB()
  store.storeDB(d)
  store.deleteDB()	
