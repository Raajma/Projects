import numpy as np
import pandas as pd
from flask import Flask,request,render_template,jsonify
import os
import json
import requests
import nltk
from textblob import TextBlob
from flask_cors import CORS
import re

def analysis(text):
    result=[]
    blob = TextBlob(text)
    for sentence in blob.sentences:
        result.append(sentence.sentiment.polarity)
    return result[0]


app=Flask(__name__)
CORS(app)


def extract_vaccine(country):
  vaccine=["vaccination","immunization","immunisation","immunize","immunise","vaccine","shots"]
  cor_query=["covid","corona","pandemic"]
  apiKey='c7293a69129743bdb461ec8142c156fa'
  sources={'india':['the-times-of-india','reuters','the-hindu','al-jazeera-english'],'us':['cnn','nbc-news','fox-news','cbs-news','techcrunch',
                                             'engadget','al-jazeera-english','mashable','independent',
                                             'the-verge','reuters'],
                                             'canada':['cbc-news',"vice-news",'reuters','the-globe-and-mail']
                                             }

  url='http://newsapi.org/v2/everything?apiKey='+apiKey
  #parameters for newsAPI
  para={'pagesize':10,'q': country+' AND ('+' OR '.join(cor_query)+') AND ('+(' OR '.join(vaccine))+')','sources':sources[country]}
  #para={'pagesize':pageSize,'q': 'onatario','sortBy':'relevancy','sources':sources}
  links=[]
  r = requests.get(url,params=para)
  
  req=r.json()
  sentiment=[]
  
  #print(req)
  # print(len(req['articles']))

  for i in req['articles']:
      links.append({'url':i['url'],'title':i['title'],'description':re.sub("<[^>]*>",'',i['description']),
        'image_url': i['urlToImage'],'sentiment':analysis(i['description']),
        })
  return links

@app.route('/initial',methods=['POST','GET'])
def general_news():
  news=pd.read_csv('general.csv')
  res={'data':[]}
  for index,i in news.iterrows(): 
    res['data'].append({'title':i['title'],
      'description':i['description'],'url':i['url'],'image_url':i['image_url']
      ,'sentiment':i['sentiment']})
      
  return jsonify(res)

@app.route('/',methods=['POST','GET'])
def extractor():
  req=request.get_json(force=True)
  city=req.get('city')
  if(req.get('category')=='vaccine'):
    res={}
    links=extract_vaccine(req.get('country'))
    res[req.get('country')]=links
    return jsonify(res);

  data=pd.read_csv('news.csv')
  country_result=data[data['country']==req.get('country')]
  res=country_result[country_result['category']==req.get('category')]
  if(city!=None):
    res=res[res['city']==city]
  
  #print(res)
  categories=res.columns
  result={}

  for index,i in res.iterrows(): 
    while True:
      try:
        result[i['city']].append({'country':i['country'],'category':i['category'],'title':i['title'],
          'description':i['description'],'url':i['url'],'image_url':i['image_url']
          ,'sentiment':i['sentiment']})
        break;
      except:
        result[i['city']]=[]

  #print(result)
  # need to convert to json format
  return jsonify(result);

if(__name__=='__main__'):
  app.run(host='0.0.0.0',port=2222,debug=True)
