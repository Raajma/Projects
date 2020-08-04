import requests
import json
from flask import Flask, jsonify,request
import pandas as pd
from flask_cors import CORS

flask_b=Flask("__main__")
CORS(flask_b)
apiKey = 'AIzaSyAY0Ebwv640AVUvKyQXnK2W_nxXIORMRhE'

@flask_b.route("/",methods=['GET'])
def reqst():

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    inp = request.get_json(force=True)
    req = requests.get( url + 'query=schools near ' + inp['code'] +
                   '&key=' + apiKey)


    data = req.json()
    # print(data)
    result = data['results']
    # store all result in json

    data_b=[]
    data_f=[]
    school=[]
    for i in range(len(result)):
      data_b.append(result[i]['business_status'])
      data_f.append(result[i]['formatted_address'])
      #append the school name
      # add necessary details.


    data={'business_status':data_b,"formatted_address":data_f}
    # update the necessary lists in data object.
    return jsonify(data)
    

flask_b.run(host='0.0.0.0',port=7070,debug=True)
