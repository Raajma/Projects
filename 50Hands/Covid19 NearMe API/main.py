import requests
import json
from flask import Flask, jsonify,request
import pandas as pd
#from flask_cors import CORS

app = Flask("__main__")
#CORS(flask_b)

apiKey = 'AIzaSyDmmcL8vOEOdKoMUGyvpI2VTz4mUC4TmLg'     #Sherin's API Key. 
# apiKey = 'AIzaSyAY0Ebwv640AVUvKyQXnK2W_nxXIORMRhE'   # Eliyas's API Key.


@app.route("/",methods=['GET'])
def reqst():

  url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

  inp = request.get_json(force=True)
  # Request format {"code":"pincode", "category": "schools"}

  # Reading existing database.
  db = pd.read_csv('data.csv')
  exist_in_db = db[(db['pincode'] == inp['code'] )& (db['category'] == inp['category'])]

  if len(exist_in_db) == 0:
    print("Pin code and category not found in DB")  
    # Hence store the query's results in the csv. 
    req = requests.get( url + 'query='+inp['category']+'near ' + inp['code'] + '&key=' + apiKey)
    # Tested the query with pincodes in Chennai and cities in Canada. 
    
    data = req.json()
    result = data['results']
    status = []
    # address = []
    school_names = []
    length = len(result)
    for i in range(length):
      # Append information.
      status.append(result[i]['business_status'])
      # address.append(result[i]['formatted_address'])
      school_names.append(result[i]['name'])
    
    data = { 'pincode':[inp['code']]*length, 'category': [str(inp['category'])]*length, 'status': status, 'name':school_names}
    response = { 'status': status, 'name':school_names }
    df = pd.DataFrame.from_dict(data)
    df.to_csv("data.csv", index=False, mode='a', header=False)
  
  else: 
    # The entered pin code and category exist in the db.
    print("Pincode and category found in DB")
    response = { 'status' : exist_in_db['status'].values.tolist(), 'name': exist_in_db['name'].values.tolist() } 
  
  return jsonify(response)
    

app.run(host='0.0.0.0',port=5000,debug=True)

