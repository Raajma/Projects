import pandas as pd
import numpy as np
import geopy
import time
from sqlalchemy import create_engine


india=pd.read_csv('data/india-cities.csv')['City'].values.tolist()[:20]
canada=pd.read_csv('data/canada-cities.csv')['City'].values.tolist()[:20]
us=pd.read_csv('data/usa-cities.csv')['City'].values.tolist()[:50]


def getLocation(country):
	location=[]
	data=pd.DataFrame();
	for i in country:
		while(True):
			try:
				loc=getLocationCoordinates(i);
				location.append([loc[0],loc[1]]);
				break;
			except:
				time.sleep(0.1)

		data=data.append({'city':i,'lat':loc[0],'lon':loc[1]},ignore_index=True)

	return data

def getLocationCoordinates(locationName):
  locator = geopy.geocoders.Nominatim(user_agent='demo')
  location = locator.geocode(locationName)

  return (location.latitude,location.longitude)

if(__name__=='__main__'):
	data=pd.DataFrame()
	locator = geopy.geocoders.Nominatim(user_agent='demo')
	data=data.append(getLocation(india),ignore_index=True)
	data=data.append(getLocation(canada),ignore_index=True)
	data=data.append(getLocation(us),ignore_index=True)

	con = create_engine('mysql+pymysql://u831388458_covid19:Password@123@34.89.97.3:3306/u831388458_covid19stats') 
	
	data.to_sql('cities_nlp', con, if_exists='replace')

