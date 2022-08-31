import sqlite3

con = sqlite3.connect("GroupProject2.db")
cur = con.cursor()

cur.execute("CREATE TABLE users(login, password)")
cur.execute("CREATE TABLE progress(user_id,movie_id,state,percent)")
cur.execute("INSERT INTO users(login,password) VALUES('username','password')")

con.commit()
cur.close()
con.close()
