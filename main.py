#Author: Chatchawal Sangkeettrakarn
#Date: September 20,2020.

from fastapi import FastAPI , Form ,File, UploadFile
import uvicorn
import numpy as np
import re
import math
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse
from pythainlp import word_tokenize
import pandas as pd

app = FastAPI()

@app.post("/cleaning")
def cleaning(text):
  clist =  "'\"“”‘’()[]" 
  # clist = ['"',"'", "“","”","‘","’","(",")","[","]"]
  cdict = {
  '"' : '"',
  "'": "'",
  "“": "”",
  "‘": "’",
  "(":")",
  "[": "]"
  }

  list_cleaning = []
  x = 0
  y = 0
  state =0
  state_s_d = 0
  # for x in df[0:20].iterrows():
  #   text = x[1].title
  for i,c in enumerate(text):
      if c  not in clist:
        continue
      else:
        # print(c,'--->',cdict.get(c))
        if (c  in cdict and state == 0):
          e = cdict.get(c)
          x = i
          state = 1 
          print (c)
          continue
         
        if (c != e and state != 1 ):
            # print (e)
          continue
        else:
          # print (e)
          y = i
          t = text[x + 1: y]  
          t = t.strip(" ")
          list_cleaning.append(t)
          x = 0
          y = 0
          state = 0
          continue
  return list_cleaning   

@app.post("/files/")
async def create_file(file: bytes = File(...)):
   return {
      "file_size": len(file)
   }
   
@app.post("/cleaning_file")
def cleaning_file(xlsx_file: UploadFile = File(...)):
    if xlsx_file.filename.endswith('.csv') or xlsx_file.filename.endswith('.xlsx'):
        df = pd.read_excel(xlsx_file.file)
        clist =  "'\"“”‘’()[]" 
        # clist = ['"',"'", "“","”","‘","’","(",")","[","]"]
        cdict = {
        '"' : '"',
        "'": "'",
        "“": "”",
        "‘": "’",
        "(":")",
        "[": "]"
        }

        list_cleaning = []
        x = 0
        y = 0
        state =0
        state_s_d = 0
        # for x in df[0:20].iterrows():
        #   text = x[1].title
        for x in df[0:20].iterrows():
            text = x[1].title
            for i,c in enumerate(text):
                if c  not in clist:
                  continue
                else:
                    # print(c,'--->',cdict.get(c))
                  if (c  in cdict and state == 0):
                    e = cdict.get(c)
                    x = i
                    state = 1 
                    print (c)
                    continue
                    
                  if (c != e and state != 1 ):
                        # print (e)
                    continue
                  else:
                      # print (e)
                    y = i
                    t = text[x + 1: y]  
                    t = t.strip(" ")
                    list_cleaning.append(t)
                    x = 0
                    y = 0
                    state = 0
                  continue
        return list_cleaning   
    else:
        return "ไฟล์ไม่ตรงกับที่ระบบต้องการ"

@app.get("/Ronnakon")
def Ronnakon(text):
    return word_tokenize(text)

@app.get("/len")
async def add(a):
    return len(a)

def result(res):
    return {"result":res}

@app.get("/")
async def main():
    return 'Hello World'

@app.get("/test")
async def test():
    return 'Test Tutorial'

@app.get("/add")
async def add(a: int = 0, b: int = 0):
    return a+b

@app.get("/mul")
async def mul(a: int = 0, b: int = 0):
    return a*b

@app.get("/pow")
async def pow(a: int = 0, b: int = 0):
    return math.pow(a,b)


def tonumlist(li):
    ls = li.split(',')
    for i in range(len(ls)):
        ls[i] = float(ls[i])
    return list(ls)

@app.get("/asc")
async def asc(li):
    ls = tonumlist(li)
    ls.sort()
    return ls

@app.get("/desc")
async def desc(li):
    ls = tonumlist(li)
    ls.sort(reverse=True)
    return ls

@app.get("/sum")
async def sum(li):
    ls = tonumlist(li)
    return np.sum(np.array(ls))

@app.get("/avg")
async def avg(li):
    ls = tonumlist(li)
    return np.average(ls)

@app.get("/mean")
async def mean(li):
    ls = tonumlist(li)
    return np.mean(ls)

@app.get("/max")
async def max(li):
    ls = tonumlist(li)
    return np.amax(ls)

@app.get("/min")
async def min(li):
    ls = tonumlist(li)
    return np.amin(ls)

@app.get("/validation-ctzid")
async def validation_ctzid(text):
    if(len(text) != 13):
        return False
    
    sum = 0
    listdata = list(text)
    
    for i in range(12):
        sum+=int(listdata[i])*(13-i)

    d13 = (11-(sum%11))%10
        
    return d13==int(listdata[12])

@app.get("/validation-email")
async def validation_email(text):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex,text):
        return True
    else:
        return False
    
    
@app.get("/google-search",response_class=PlainTextResponse)
def google_search(text):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    url = 'https://www.google.com/search?q=' + str(text)
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    t = soup.findAll('div', {'class':"r"})
    i = 0
    result = ''
    for a in t:
        href = a.a['href']
        head = a.h3.text
        result = result + head + '<br>' + href + '<br><br>'
        i += 1
        if(i >= 5):
            break
    
    return(result)




if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 