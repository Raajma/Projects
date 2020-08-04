import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import geopy
import pandas as pd
import time 
from datetime import date
from sqlalchemy import create_engine

limit=30
key_ind=0
count=1000
key=['52wj556HeFLCzGaegDrsI8IHh','yGyyJ3Wjmz40bbGCNZER8JvUe','kMIs2ofZvP81NPGpZvdYJdHPN','52wj556HeFLCzGaegDrsI8IHh','yGyyJ3Wjmz40bbGCNZER8JvUe',
	'fNleHzoZTPNQYHVpxcz2Rr50V','KTRy9UXII4G0JmJIJzg44FgB5',
	'8DPg1QwKV3R76zR1SgJhdWXGx']

secret_key=['3S29eLJePI5f2JO3U4PjaRpESdNurzPHQkcpm20iUkd38kK95g','WtlOdGMp32iGd6uJB6qNwRAN6eXQYhsPq7feFWn6NKpLzs1f7H','ZNxj2WGLuJgVqmlHQKfG8s65ODC8mWbf0wXnsDPr4EqL2gsSni','3S29eLJePI5f2JO3U4PjaRpESdNurzPHQkcpm20iUkd38kK95g','WtlOdGMp32iGd6uJB6qNwRAN6eXQYhsPq7feFWn6NKpLzs1f7H',
			'S8bA73lqE9Gal8lKrGMIrgqEQgVp8cwwmBrUuBxqfxnI4Hd3mQ','crEVdFb0g5yY1u6MG1o7dHQ3jhfI0g3G7e8QbRPYcYWhtvxuLX',
			'DQUkXst8mKEG3kIg1DUfs0uIc6TE6vF4lCYStHbSjtTLLzffeC']

access_token=['1272818153815306240-mNrJTkuhb3m7SDYVaViKy8YSOOrlqh','1273090214970314752-MLdgtUh8dvLk4AUPGMX8vx0aU50hFw','1272817919840280577-WZAtMqfWdD0jJvXRrfazCdgeZf0Bke','1272818153815306240-mNrJTkuhb3m7SDYVaViKy8YSOOrlqh','1273090214970314752-MLdgtUh8dvLk4AUPGMX8vx0aU50hFw',
			'1273182326537834500-2AfWx04gD0Er2ncevMkiJ2en5nSge1','2330239098-WhgBS6ikNWqlf55BZkwOouC1WymiNBHZmdgJdbl',
			'610633939-uAKjkqNqolQMEH71hg7WJS37PKqKXGShDEYKy3DN']
secret_access=['f0pqpuN4fiXZs2Ar483RAvYdJ3wbB2bjiUpCeerAc1uyI','90RDBaLpGTMSNW4VanbkibK1nrP1iIEhI7xbiVT07AnEZ','b9i6E3lWdpa9qWc4ikdwTzWEaFkzSGXtlnMwmEhSHSJz3','f0pqpuN4fiXZs2Ar483RAvYdJ3wbB2bjiUpCeerAc1uyI','90RDBaLpGTMSNW4VanbkibK1nrP1iIEhI7xbiVT07AnEZ',
			'rHr6n95y99LyriMKQPP2OUC7fUItvLI6Hwe8P0rYga1mE','B9r0rpOAOYEmUVzURuOY2q3MQBDJVtspVC5YLrupePFiz',
			'5uKcfFEGUmEdWJBTQmhDqg8h62bBxQpeiMwwfeDRuS3p8']

length=len(key)

# india=pd.read_csv('data/india-cities.csv')['City'].values.tolist()[:20]
# canada=pd.read_csv('data/canada-cities.csv')['City'].values.tolist()[:20]
# us=pd.read_csv('data/usa-cities.csv')['City'].values.tolist()[:50]
vaccine=pd.read_csv('data/vaccine-list.csv')['name'].values.tolist()


def getLocationCoordinates(locationName):
  locator = geopy.geocoders.Nominatim(user_agent='demo')
  location = locator.geocode(locationName)

  return (location.latitude,location.longitude)

locator = geopy.geocoders.Nominatim(user_agent='demo')


class Twitter:
	# def __init__(self):
	# 	self.consumer_key = '8DPg1QwKV3R76zR1SgJhdWXGx'
	# 	self.consumer_secret = 'DQUkXst8mKEG3kIg1DUfs0uIc6TE6vF4lCYStHbSjtTLLzffeC'

	# 	self.access_token = '610633939-uAKjkqNqolQMEH71hg7WJS37PKqKXGShDEYKy3DN'
	# 	self.access_token_secret = '5uKcfFEGUmEdWJBTQmhDqg8h62bBxQpeiMwwfeDRuS3p8'


	# 	#Making the Authentication Process
	# 	auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
	# 	auth.set_access_token(self.access_token,self.access_token_secret)
	# 	self.api = tweepy.API(auth, wait_on_rate_limit=True)

	def authenticate(self,consumer_key,consumer_secret,access_token,access_token_secret):
		#Making the Authentication Process
		auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
		auth.set_access_token(access_token,access_token_secret)
		self.api = tweepy.API(auth, wait_on_rate_limit=True)

	def getTweets(self,location,v,count=1000):
		res=[]
		search_term = [v]
		if count==0:
			#fetching all tweets
			tweets = tweepy.Cursor(self.api.search,q=search_term,lang='en',result='popular',geocode=location).items()
			for i in tweets:
				res.append(i.text)
		else:
			#fetching the specified number of tweets
			tweets = tweepy.Cursor(self.api.search,q=search_term,lang='en',result='popular',geocode=location).items(count)
			for i in tweets:
				res.append(i.text)

		return res

class SentimentAnalyser:

	def removeHyperlinks(self,text):
		text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split()) 
		return text

	def vaderSentiment(self,text):
		text = self.removeHyperlinks(text)
		analyzer = SentimentIntensityAnalyzer()
		score =  analyzer.polarity_scores(text)
		if score['compound']>0:
			return ('Positive',score['compound'])
		elif score['compound']<0:
			return ('Negative',score['compound'])
		else:
			return ('Neutral',score['compound'])


def extract(country,name):
	key_ind=4
	global loc
	global location
	global twitterObject
	tweet_result={'country':[],'polarity_score':[],'medicine':[]}

	for i in country:
		loc=(0.0,0.0)
		while(True):	
			try:
				loc=getLocationCoordinates(i);
				location=str(loc[0])+","+str(loc[1])+",7000km";
				break;
			except:
				time.sleep(1)
		print(location)

		for v in vaccine:
			tweet_list=[]
			while(True):
				try:
					twitterObject = Twitter()
					twitterObject.authenticate(key[key_ind],secret_key[key_ind],access_token[key_ind],secret_access[key_ind])
					tweet_list = twitterObject.getTweets(location,v,count)	
					break;
				except Exception as e:
					print(e)
					print('Out of Requests!')
					key_ind+=1;
					if(key_ind==length):
						print('Ran out of All Requests!')
						key_ind=0
						break;

			sa = SentimentAnalyser()
			avg=0
			num=0
			for tweet in tweet_list:
				output = sa.vaderSentiment(tweet)
				avg+=output[1]
				num+=1

			
			tweet_result['country'].append(i)
			if(num!=0):
				tweet_result['polarity_score'].append((avg/num))
			else:
				tweet_result['polarity_score'].append(0.000);
			
			tweet_result['medicine'].append(v)
	return tweet_result

def tweetSentiment():
	print('Started!')
	tweet_india=extract(['usa','india','canada'],'country')
	#print(tweet_india)
	#res=pd.DataFrame(columns=['country','city','tweet','polarity_score','sentiment-label','lat','lon'])
	res=[]
	country=[]
	#city=[]
	tweet=[]
	polarity=[]
	sentiment=[]
	lat=[]
	lon=[]
	medicine=[]
	# print(len(tweet_india['country']))
	# print(tweet_india)
	try:
		for ind in range(len(tweet_india['medicine'])):
			country.append(tweet_india['country'][ind])
			polarity.append(tweet_india['polarity_score'][ind])
			medicine.append(tweet_india['medicine'][ind])

	except Exception as e:
		print(e)

	res.append(pd.DataFrame({'country':country,
	 		'polarity_score':polarity,
	 		'medicine':medicine,
	 		'date':[date.today() for _ in range(len(polarity))]}))

	#data=pd.read_csv('twitter.csv')
	con = create_engine('mysql+pymysql://u831388458_covid19:Password@123@34.89.97.3:3306/u831388458_covid19stats') 
	
	data=pd.DataFrame()
	data=data.append(res)


	data.to_sql('vaccine_tsa', con, if_exists='append')
	#data.to_csv('twitter.csv',index=False)

	print('Extraction Completed!')


if __name__ == '__main__':
	tweetSentiment();
	print('done')
