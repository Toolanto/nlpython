# Developer Antonio Luca
# coding=utf-8

import sqlite3
import re
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
    TABLE = "CREATE TABLE corpus (id varchar, document text)"
    conn.execute(TABLE)
  
  def storeDB(self, csvHandler):
    conn = sqlite3.connect(self._namedb)
    c = conn.cursor()
    for document in csvHandler.readconcactString():
      ident = document[0]
      if ident == '':
        ident = random.randint(0,100000)
      text = document[1]
      #verifico se nel documento ci sono caratteri speciali es. "word" -> \"word\"
      pattern = "\""
      text = re.sub(pattern,'"',text)
      pattern = "\\'"
      text = re.sub(pattern,"''",text) 
      #QUERY = "INSERT INTO corpus VALUES ({0},\'{1}\')".format(ident,text[1:len(text)-1].encode('utf-8'))
      QUERY = "INSERT INTO corpus VALUES (?,?)"
      c.execute(QUERY,(ident,text[1:len(text)-1]))
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
    return [row[0] for row in c.execute("SELECT document FROM corpus WHERE id==?",var)]

  def searchAll(self):
    conn = sqlite3.connect(self._namedb)
    c = conn.cursor()
    return [row for row in c.execute("SELECT * FROM corpus")]
    
  
