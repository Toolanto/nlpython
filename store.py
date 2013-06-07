# Developer Antonio Luca

import sqlite3
import random

class Store:
  def makeDB(self): pass
  def storeDB(self): pass
  def deleteDB(self): pass

class StoreCorpus(Store):        
  
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
      if len(ident)== 0:
        ident = random.randint(0,100000)
      print ident
      text = document[1]
      QUERY = "INSERT INTO corpus VALUES ({0},\'{1}\')".format(ident,text)
      c.execute(QUERY)
      conn.commit()
  
  def deleteDB(self):
    conn = sqlite3.connect(self._namedb)
    QUERY = "DROP TABLE corpus"
    c = conn.cursor()
    c.execute(QUERY)
  
  def searchByIdentifier(self,identifier):
    var = (identifier,)
    conn = sqlite3.connect(self._namedb)
    c = conn.cursor()
    return [row for row in c.execute("SELECT document FROM corpus WHERE id==?",var)]

  def searchAll(self):
    conn = sqlite3.connect(self._namedb)
    c = conn.cursor()
    return [row for row in c.execute("SELECT * FROM corpus")]
    
  
