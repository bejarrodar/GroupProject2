import sqlite3

import pandas as pd
from sqlalchemy import create_engine

sql = 'sqlite+pysqlite:///GroupProject2.db'
engine = create_engine(sql)

users = pd.DataFrame({'user_id':[],'login':[],'password':[]})
progress = pd.DataFrame({'user_id':[],'movie_id':[],'status':[],'percent':[]})
admins =  pd.DataFrame({'admin_id':[0],'login':['admin'],'password':['password']})

users.to_sql("users",engine,if_exists='replace')
progress.to_sql("progress",engine,if_exists='replace')
admins.to_sql("admins",engine,if_exists='replace')
