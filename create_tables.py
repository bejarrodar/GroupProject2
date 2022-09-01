import sqlite3

con = sqlite3.connect("GroupProject2.db")
cur = con.cursor()
cur.execute("DROP TABLE users")
cur.execute("DROP TABLE progress")
cur.execute("CREATE TABLE users(user_id,login, password)")
cur.execute("CREATE TABLE progress(user_id,movie_id,state,percent)")
cur.execute("INSERT INTO users(login,password) VALUES('username','password')")
cur.execute("CREATE TABLE admins(admin_id,login,password)")
cur.execute("INSERT INTO admins(admin_id,login,password) VALUES(1,'admin','password')")

con.commit()
cur.close()
con.close()
