import sqlite3

import pandas as pd
from sqlalchemy import create_engine

sql = 'sqlite+pysqlite:///GroupProject2.db'
engine = create_engine(sql)

data = pd.read_csv('movies_metadata.csv')

data = data[['id','genres','original_title']]

data.rename(columns={'id':'movie_id'})

data.to_sql('movies',engine)
