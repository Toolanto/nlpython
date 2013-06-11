# Developer Antonio Luca
# coding=utf-8

import csv
import codecs

class CustomDialect(csv.Dialect):
  delimiter = ','
  quotechar = '"'
  lineterminator ='\r\n' 
  quoting = csv.QUOTE_NONE 

class AbstractCSV:
  def reader(self):pass

class CSVHandler:
  def __init__(self,path,dialect = CustomDialect):
    self._path = path
    self._dialect = dialect

  def reader(self):
    uf = codecs.open(self._path,'rb','utf-8')
    self._documents = [(c[0],c[1:]) for c in unicode_csv_reader(uf,self._dialect)]
    stringjoin = self._dialect.delimiter
    self._documents = [[testo[0], stringjoin.join([term for term in testo[1]])] for testo in self._documents]
    return self._documents

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

if __name__=="__main__":
  from store import *
  d = CSVHandler("document.txt")
  #encode utf-8 in str
  #for text in d.reader():
  #  print text[0]#,text[1].encode('utf-8')
  print d.reader()[0]

 
