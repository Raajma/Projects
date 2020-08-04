from datetime import date
from datetime import timedelta
import pandas as pd
import datetime
import numpy as np
import os

data=pd.read_csv('db_final.csv')
# print(date.today()-timedelta(days=1))

dates=data['date']
res=[]
for i in range(90):
	res.append((date.today()-timedelta(days=1)).strftime("%d-%m-%Y"))

for i in range(91,181):
	res.append((date.today()).strftime("%d-%m-%Y"))
data['date']=np.array(res)

os.remove('db_final.csv')
data.to_csv('db_final.csv',index=False)