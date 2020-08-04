import requests
import json

url = ('http://newsapi.org/v2/everything?q=chennai&q=covid&sortBy=popularity&apiKey=c7293a69129743bdb461ec8142c156fa')

response = requests.get(url)

res=response.json()