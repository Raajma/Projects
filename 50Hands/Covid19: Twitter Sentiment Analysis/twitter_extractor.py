from flask import Flask,render_template,jsonify,request
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import geopy
import pandas as pd
from flask_cors import CORS
import time
from datetime import date

def getLocationCoordinates(locationName):
  locator = geopy.geocoders.Nominatim(user_agent='demo')
  location = locator.geocode(locationName)

  return (location.latitude,location.longitude)


app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
def tweetSentiment():
	content = request.get_json()
	try:
		while(True):
			loc=getLocationCoordinates(content['location']);
			break;
	except:
		time.sleep(1)
	data=pd.read_csv('twitter.csv')
	city=content.get('city')
	result={}
	mn=999
	count=20   # Number of extracted tweets for each city
	# for i in range(0,len(data['lat']),count):
	# 	if(abs(loc[0]-data['lat'][i])+abs(loc[1]-data['lon'][i]) < mn):
	# 		mn=abs(loc[0]-data['lat'][i])+abs(loc[1]-data['lon'][i])
	# 		city=data['city'][i]
	res=data[data['country']==content.get('country')]
	res=data[data['city']==city]
	dt=[]
	for index,i in res.iterrows():
		dt.append({'country':i['country'],
			'city':i['city'],
			# 'lat':i['lat'],
			# 'lon':i['lon'],
			'polarity_score': i['polarity_score'],
			'date':i['date']})
	result['data']=dt

	return jsonify(result)

if(__name__=='__main__'):
	app.run(host='0.0.0.0',port=2211,debug=True)