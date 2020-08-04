
from sqlalchemy import create_engine
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://u831388458_covid19:Password@123@213.190.6.106/u831388458_covid19stats'
db_connection = create_engine(db_connection_str)

df = pd.read_sql('SELECT * FROM case_history_by_province', con=db_connection)

print(df.head())

df.to_csv('case_history.csv',index=False)