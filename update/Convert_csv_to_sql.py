import sqlite3

import pandas as pd
from sqlalchemy import create_engine

sql = 'sqlite+pysqlite:///GroupProject2.db'
engine = create_engine(sql)

data = pd.read_csv('movies.csv')

data = data[['id','genres','original_title']]
data = data[data['id'].apply(lambda x: str(x).isdigit())]
data['id']=pd.to_numeric(data['id'], downcast='integer', errors='coerce')


data.dropna(inplace=True)
data.rename(columns={'id':'movie_id'},inplace=True)
data.astype({'movie_id': 'int64'})
data.rename(columns={'id':'movie_id'},inplace=True)
data["genres"] = data["genres"].str.replace(" ","")
data["genres"] = data["genres"].str.replace(",,",",")
data["genres"] = data["genres"].str.lstrip(",")

data.to_sql('movies',engine,if_exists='replace')
