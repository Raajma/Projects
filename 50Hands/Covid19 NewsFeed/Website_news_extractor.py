from flask import Flask,render_template,request,jsonify
import requests
from flask_cors import CORS
import os
import json
from datetime import datetime

def extract_urls(country,pageSize,apiKey,queries,cor_query,sources):
  url='http://newsapi.org/v2/everything?apiKey='+apiKey
# parameters for newsAPI
  para={'pagesize':pageSize,'q': country+' AND ('+' OR '.join(cor_query)+') AND ('+(' OR '.join(queries))+')','sortBy':'relevancy','sources':sources}
  links=[]
  #print(country+' AND ('+' OR '.join(cor_query)+') AND ('+(' OR '.join(queries))+')')
  r = requests.get(url,params=para)
  req=r.json()
  # print(req)
  #print(len(req['articles']))
  for i in req['articles']:
      links.append({'url':i['url'],'title':i['title'],'description':i['description'],
        'image_url': i['urlToImage']})

  return links

app=Flask(__name__)

apiKey='348c14bd6ca44c0ba61107ec4947eb0a'

@app.route('/extract',methods=['POST','GET'])
def extract():
    #return "This works";
    try:
        request_data = request.get_json(force=True)
        countryName = request_data.get("country")
        categoryType = request_data.get("category")

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

        if(categoryType =='finance'):
            data=extract_urls(countryName,20,apiKey,financial,covid,sources[countryName])
        elif(categoryType =='vaccine'):
            data=extract_urls(countryName,20,apiKey,vaccine,covid,sources[countryName])
        elif(categoryType =='policies'):
            data=extract_urls(countryName,20,apiKey,policies,covid,sources[countryName])
        elif(categoryType =='cases'):
            data=extract_urls(countryName,20,apiKey,cases,covid,sources[countryName])
        elif(categoryType == 'crime'):
            data=extract_urls(countryName,20,apiKey,crimes,covid,sources[countryName])
    
    
        data_dict=dict()
        data_dict['data']=data
        data_json=json.dumps(data_dict)
        return data_json

    except:
        url='https://newsapi.org/v2/everything?apiKey='+apiKey
        para={'pagesize':9,'q': ' OR '.join(["covid","corona","pandemic"])}
        r = requests.get(url,params=para)
        req=r.json()
        #print(req)
        links=[]
        #print(len(req['articles']))

        for i in req['articles']:
          #print(i)
          links.append({'url':i['url'],'title':i['title'],'description':i['description'],
            'image_url': i['urlToImage']})

        data_dict=dict()
        data_dict['data']=links
        data_json=json.dumps(data_dict)
        return data_json


if(__name__== '__main__'):
    app.run(host='0.0.0.0',port=555)

