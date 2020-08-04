import time 
from datetime import date
from sqlalchemy import create_engine
import pandas as pd
from datetime import date

con = create_engine('mysql+pymysql://u831388458_covid19:Password@123@34.89.97.3:3306/u831388458_covid19stats') 

data=pd.read_sql_table('twitter_nlp',con)

data.to_csv('tweets_sofar.csv',index=False)

# data=pd.read_csv('tweets_sofar.csv')
# country=[]
# city=[]
# avg=[]
# for i in range(90):
# 	tmp=data[data['city']==data['city'][i]]
# 	country.append(tmp['country'].iloc[0])
# 	city.append(tmp['city'].iloc[0])
# 	avg.append(tmp['polarity_score'].mean())

# first_july=pd.DataFrame({'country':country,
# 									'city':city,
# 									'date':['04-07-2020' for i in range(len(country))],
# 									'polarity_score':avg})

# first_july.to_csv('missed.csv',index=False)

# data=pd.read_csv('tweets_sofar.csv')
# july=pd.read_csv('first_july.csv')
# res=data.append(july)
# res=res.sort_values(by=['date'],ascending=True)

# res.to_csv('final.csv',index=False)
# res=pd.read_csv('tweets_sofar.csv')
# res.to_sql('twitter_nlp', con, if_exists='append')
