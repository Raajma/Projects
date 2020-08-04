import requests, json 
from flask import Flask,jsonify,request
import geopy

import os
import pandas as pd
import csv

app = Flask(__name__)




def getLocationCoordinates(locationName):
  locator = geopy.geocoders.Nominatim(user_agent='lat and lng finder')
  location = locator.geocode(locationName,timeout=180)

  return (location.latitude,location.longitude)


def getFromDB(db,pincode,category):
	out=[]
	for i in db.values:
		if str(i[1])==pincode and i[3] == category:
			result={}
			result['name'] = str(i[0])
			result['is_open'] =str( i[2])
			out.append(result)
	return out


def checkDB(db,pincode,category):
	for i in db.values:
		if str(i[1])==pincode and i[3]==category:
			return True
	return False

def getPinCode(loc):
	locator = geopy.geocoders.Nominatim(user_agent='pincode finder')
	location = locator.reverse(loc,timeout=180)
	return str(location.raw['address']['postcode'])

@app.route('/nearMe',methods=['GET','POST'])
def getLocationStatus():
	APIKEY = 'AIzaSyAY0Ebwv640AVUvKyQXnK2W_nxXIORMRhE'

	content = request.json
	types = content['category']
	city_name = content['city_name']
	pagetoken = None
	if "radius" in content.keys():
		radius = content['radius']
	else:
		radius = 4000
	lat,lng = getLocationCoordinates(city_name)
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={types}&key={APIKEY}{pagetoken}".format(lat = lat, lng = lng, radius = radius, types = types,APIKEY = APIKEY, pagetoken = "&pagetoken="+pagetoken if pagetoken else "")

	PATH = './data.csv'
    
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		print('File Exists')

	else:
		print("File is Missing --  Creating a New File")
		with open('data.csv', 'w', newline='') as fp:
			a = csv.writer(fp, delimiter=',')
			data_head = [['name', 'pincode', 'status', 'category']]
			a.writerows(data_head)
		print("File Created")

	db = pd.read_csv('data.csv')

	if len(db) == 0 or not checkDB(db,content['pincode'],types):
		print("Data Doesnt Exist in the data.csv file . So making the API request")
		response = requests.get(url)	
		res = json.loads(response.text)
		out =[]


		count=0
		df = pd.read_csv("data.csv")
		for i in range(len(res['results'])):
			result={}
			if 'opening_hours' in res['results'][i].keys():
				#result['business_status']=res['results'][i]['business_status']
				if res['results'][i]['opening_hours']['open_now']==True:
					result['is_open']= "Open"
				else:
					result['is_open']= "Closed"  
				result['location_name']=res['results'][i]['name']
				query = str(res['results'][i]['geometry']['location']['lat'])+","+str(res['results'][0]['geometry']['location']['lng'])
				pincode = getPinCode(query)
				print(pincode)
				db_data={}
				db_data = {
				'name':result['location_name'],
				'pincode':pincode,
				'category':types,
				'status':str(result['is_open'])
				}
				
				df = df.append(db_data,ignore_index=True)
				count+=1
				
				out.append(result)
		print("count : ",count)
		df.to_csv("data.csv", index = False, mode='a', header=False)
		return jsonify(out)
	else:
		print("Data present in the File")
		out = getFromDB(db,content['pincode'],types)
		
		return jsonify(out)

if __name__ == '__main__':
	locator = geopy.geocoders.Nominatim(user_agent='demo')
	app.run(host='0.0.0.0',port=5124,debug=True)
