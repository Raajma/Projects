
from flask import Flask,render_template,request
import requests
import os
import json
import pandas as pd
import nltk
from textblob import TextBlob
import re

def printer():
  print('Hello World!')
  
def analysis(text):
    result=[]
    blob = TextBlob(text)
    for sentence in blob.sentences:
        result.append(sentence.sentiment.polarity)
    return result[0]

def extract_urls(country,city,pageSize,apiKey,queries,cor_query,sources,category):
  url='http://newsapi.org/v2/everything?apiKey='+apiKey
  #parameters for newsAPI
  para={'pagesize':pageSize,'q': country+' AND '+city+' AND ('+' OR '.join(cor_query)+') AND ('+(' OR '.join(queries))+')','sources':sources}
  #para={'pagesize':pageSize,'q': 'onatario','sortBy':'relevancy','sources':sources}
  links=[]
  r = requests.get(url,params=para)
  
  req=r.json()
  sentiment=[]
  
  # print(req)
  # print(len(req['articles']))

  for i in req['articles']:
      links.append({'url':i['url'],'title':i['title'],'description':i['description'],
        'image_url': i['urlToImage'],'sentiment':analysis(i['description']),
        'city':city,'country':country,'category':category})
  return links

def extract_general(apiKey,cor_query,pageSize=11):
  url='http://newsapi.org/v2/everything?apiKey='+apiKey
  #parameters for newsAPI
  para={'pagesize':pageSize,'q': ' OR '.join(cor_query)}
  #para={'pagesize':pageSize,'q': 'onatario','sortBy':'relevancy','sources':sources}
  links=[]
  r = requests.get(url,params=para)
  
  req=r.json()
  sentiment=[]
  
  # print(req)
  # print(len(req['articles']))

  for i in req['articles']:
      links.append({'url':i['url'],'title':i['title'],'description':i['description'],
        'image_url': i['urlToImage'],'sentiment':analysis(i['description']),
        })
  return links

def extract():
    #country=request.form['country']
    #print(request.form)
    print('started')
    
    financial=['money','opportunity','business insider','google my business','business plan','business ideas',
                                                                'business news','income','economy','income','bbc business','small business ideas','small business',
                                                                'online business','business line','business letter','business daily','starting a business','financial news',
                                                                'business proposal','business times','profitability','business portal','big money','what is business',
                                                                'business world','starting your own business']
    vaccine=["vaccination","immunization","immunisation","immunize","immunise","vaccine","shots"]
    covid=["covid","corona","pandemic"]
    policies=["government","policy","impact","unemployment"," economic relief package", "wall street",
    "corporations","small businesses", "travel ban", "lockdown extension"]
    cases=["Coronavirus","statistics","report","COVID-19","comorbidity","incubation period","death toll","flattening the curve",
    "cases","community spread"]
    crimes=["crime","violence","police","arrest","witness","shooting"]
    sources={'india':['the-times-of-india','reuters','the-hindu','al-jazeera-english'],'us':['cnn','nbc-news','fox-news','cbs-news','techcrunch',
                                                 'engadget','al-jazeera-english','mashable','independent',
                                                 'the-verge','reuters'],
                                                 'canada':['cbc-news',"vice-news",'reuters','the-globe-and-mail']
                                                 }
    places=pd.read_csv('data/TopCities.csv')
    cities={'india':places['City'].values.tolist()[:100],
            'canada': pd.read_csv('data/cities_canada.csv')['Name'].values.tolist(),
            'us':pd.read_csv('data/cities_us.csv')['Name'].values.tolist()}

    countries=['canada','india','us']
    categories=['finance','cases','policies','crime']

    keys=[  
    '348c14bd6ca44c0ba61107ec4947eb0a','a725fa3bdc7b4de39f487f135e3567f9',
    '4234a6f96c7e4be4977204afbc6924e0','b2b43771790f4ec9a022f4c87b82fd03',
    'fc73a5c39d3148499f880045b6e19ffa','63d2a29ceb594f40b5d5dea98dd20b65',
    '115900b40dd24fbcad54ad943f2c6c55','372577a03a294f2f8283c8f855606e35',
    'a737294b51ae4267a20ee36e790c04fb','bc4ac66f8c42469496f2bb236a968c37',
    '51ecbcf0fc2a40f1ae58f9e9022e4b57','9d6e4df815174523be1f647c9ca94358']
    key_index=0
    length=len(keys)
    rqst=0
    df=pd.DataFrame()
    for i in countries:
      for j in categories:
        res=[]
        for x in range(len(cities[i])):
          while(True):
            try:
              if(key_index>length):
                print('out of requests!')
                key_index=0
                break;
              if(j=='crime'):
                res.append(extract_urls(i,cities[i][x],10,keys[key_index%length],crimes,covid,sources[i],'crime'))
              elif(j=='finance'):
                res.append(extract_urls(i,cities[i][x],10,keys[key_index%length],financial,covid,sources[i],'finance'))
              elif(j=='policies'):
                res.append(extract_urls(i,cities[i][x],10,keys[key_index%length],policies,covid,sources[i],'policies'))
              elif(j=='cases'):
                res.append(extract_urls(i,cities[i][x],10,keys[key_index%length],cases,covid,sources[i],'cases'))
              break;
            except Exception as es:
              key_index+=1
          
        c=[]
        cate=[]
        urls=[]
        titles=[]
        desc=[]
        city=[]
        image_url=[]
        sentiments=[]
        for ind in range(len(res)):
          for i2 in range(len(res[ind])):
            c.append(res[ind][i2]['country'])
            cate.append(res[ind][i2]['category'])
            city.append(res[ind][i2]['city'])
            urls.append(res[ind][i2]['url'])
            titles.append(res[ind][i2]['title'])
            desc.append(re.sub("<[^>]*>",'',res[ind][i2]['description']))
            image_url.append(res[ind][i2]['image_url'])
            sentiments.append(res[ind][i2]['sentiment'])
            # data=pd.DataFrame({'country':i,'category':j,'url': res[ind][i2]['url'],'title':res[ind][i2]['title'],
            # 'description':res[ind][i2]['description'],'image_url':res[ind][i2]['image_url'],
            # 'sentiment':[res[ind][i2]['sentiment']]})
          
        df=df.append(pd.DataFrame({'country':c,'category':cate,'url': urls,'title':titles,
          'description':desc,'image_url':image_url,'sentiment':sentiments,
          'city':city}));
    ind=0
    while(True):
      try:
        if(ind==length):
          break;
        general=pd.DataFrame(extract_general(keys[ind%length],covid))
        general.to_csv('general.csv',index=False)
        break;
      except:
        ind+=1
    

    df.to_csv('news.csv',index=False)
    print('Extraction Completed!')

    
#if(__name__== '__main__'):
#     nltk.download('punkt')
#     extract()
#     print('Extraction Completed!')
    
