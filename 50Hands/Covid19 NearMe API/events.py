import requests
import json
from flask import Flask,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



def get_event(location,radius="25",user_key="k6fKng2JDPmpqfKW"):
	url = "http://api.eventful.com/json/events/search?"
	url += "&app_key=" + user_key
	url += "&location=" + location
	#url += "&category=" + category
	url += "&within" + radius
	url += "&page_size=250"
	url += "&sort_order=popularity"
	url += "&sort_direction=descending"
	url += "&units=km"

	events = requests.get(url).json()
	return events


@app.route("/events",methods=['GET','POST'])
def eventsAPI():
	content = request.json
	loc = content['location']

	events = get_event(loc)

	if events['events'] == None:
		return jsonify([{'status':'False'}])
	else:
		result={}
		result['status'] = "True"
		output =[result]

		for event in events['events']['event']:
			result={}
			result['event_name'] = event['title']
			result['event_venue'] = event['venue_name']
			result['country_name'] = event['country_name']
			result['region_name'] = event['region_name']
			result['city_name'] = event['city_name']
			result['start_time'] = event['start_time']
			result['end_time'] = event['stop_time']
			result['event_url'] = event['url']
			output.append(result)

		return jsonify(output)


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=6000,debug=True)
