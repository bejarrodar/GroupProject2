import sqlite3

import pandas as pd
from sqlalchemy import create_engine

sql = 'sqlite+pysqlite:///GroupProject2.db'
engine = create_engine(sql)

movies = pd.read_sql("SELECT * FROM movies",engine,index_col='id')
users = pd.read_sql("SELECT * FROM users",engine,index_col='user_id')
progress = pd.read_sql("SELECT * FROM progress",engine,index_col='user_id')
admins = pd.read_sql("SELECT * FROM admins",engine,index_col='admin_id')
movies = movies.dropna()
movies["genres"] = movies["genres"].str.replace(" ","")
movies["genres"] = movies["genres"].str.replace(",,",",")
movies["genres"] = movies["genres"].str.lstrip(",")

def search_movie(title = None,genre = None):
    if title:
        results = movies.loc[movies['original_title'].str.contains(title, case=False)]
        if not results.empty:
            return results
        else:
            print("Movie Not Found")
            cli_search()
    if genre:
        results = movies.loc[movies['genres'].str.contains(genre, case=False)]
        if not results.empty:
            return results
        else:
            print("Movie Not Found")
            cli_search()

def cli_search():
    while True:
        print("Would you like to search by:")
        print("[1] Title")
        print("[2] Genre")
        sel = input()
        try:
            sel = int(sel)
            if sel == 1 or sel == 2:
                break
            else:
                print("I didn't understand")
                print("===========================")
            break
        except ValueError:
            print("I didn't understand")
            print("===========================")
    if sel == 1:
        return search_movie(title=input("Please Enter Title: "))
    if sel == 2:
        return search_movie(genre=input("Please Enter Genre: "))

def write_sql():
    movies.to_sql("movies",engine,if_exists='replace')
    users.to_sql("users",engine,if_exists='replace')
    progress.to_sql("progress",engine,if_exists='replace')
    admins.to_sql("admins",engine,if_exists='replace')


def create_account():
    while True:
        user = input("Please enter Username: ")
        if users[users["login"].str.lower() == user.lower()].empty:
            password = input("Please enter password: ")
            print(len(users.index)+1)
            users.loc[len(users.index)] = [user,password]
            break
        else:
            print(f"The user {user} already exists")

def create_admin():
    while True:
        user = input("Please enter Admin Username: ")
        if admins[admins["login"].str.lower() == user.lower()].empty:
            password = input("Please Admin enter password: ")
            print(len(users.index)+1)
            admins.loc[len(users.index)] = [user,password]
            break
        else:
            print(f"The Admin {user} already exists")


def admin_login():
    while True:
        user = input("Please enter Admin Username: ")
        if not admins[admins["login"].str.lower() == user.lower()].empty:
            password = input("Please Admin enter password: ")
            if password == admins[admins["login"].str.lower() == user.lower()]['password'].values:
                print("Login successful")
                print(f"Welcome {user}")
                return True
            else:
                print("Incorrect Password")
        else:
            print(f"The Admin {user} could not be found")

def save_and_quit():
    write_sql()
    con = sqlite3.connect("GroupProject2.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM USERS")
    print(cur.fetchall())
    cur.close()
    con.close()

def cli_admin():
    admin = admin_login()
    if admin:
        while True:
            print("What would you like to do today?")
            print("[1] Manage Users")
            print("[2] Manage Admins")
            print("[3] Add Admins")
            inp = input()
            try:
                inp = int(inp)
                if inp in [1,2,3]:
                    break
                else:
                    print("Sorry I didn't Understand")
            except ValueError:
                print("Sorry I didn't Understand")
        if inp == 1:
            #manage Users
            manage_users(admin)
        if inp == 2:
            #manage Admins
            manage_admins(admin)
        if inp == 3:
            #add admins
            create_admin()

def manage_users(admin:bool):
    if admin:
        print("Which user do you want to change?")
        for each in users["login"].to_list():
            print(each)
        user = input()
        if not users[users["login"].str.lower() == user.lower()].empty:
            selected_user = users[users["login"].str.lower() == user.lower()]
            while True:
                print(selected_user)
                print("What would you like to change:")
                print("[1] Username")
                print("[2] Password")
                print("[3] Remove them")
                print("[4] Manage Trackers")
                sel = input()
                try:
                    sel = int(sel)
                    if sel in [1,2,3,4]:
                        break
                    else:
                        print("I didn't Understand")
                except ValueError:
                    print("I didn't Understand")
            if sel == 1:
                new = input("What would you like their new Username to be? ")
                users.loc[users["login"].str.lower() == user.lower(),"login"] = new
            if sel == 2:
                new = input("What would you like their new Password to be? ")
                users.loc[users["login"].str.lower() == user.lower(),"password"] = new
            if sel == 3:
                while True:
                    print("Are you sure you want to delete this User?")
                    print("[1] YES CANNOT BE UNDONE")
                    print("[2] NO")
                    sure = input()
                    try:
                        sure = int(sure)
                        if sure in [1,2]:
                            break
                        else:
                            print("I didn't Understand")
                    except ValueError:
                        print("I didn't Understand")
                if sure == 1:
                    users.drop(users[users["login"].str.lower() == user.lower()].index,inplace=True)
                if sure == 2:
                    manage_users(admin)
            if sel == 4:
                pass
        else:
            print("I didn't Understand")
            manage_users(admin)
        

def manage_admins(admin:bool):
    if admin:
        print("Which user do you want to change?")
        for each in admins["login"].to_list():
            print(each)
        user = input()
        if not admins[admins["login"].str.lower() == user.lower()].empty:
            selected_user = admins[admins["login"].str.lower() == user.lower()]
            while True:
                print(selected_user)
                print("What would you like to change:")
                print("[1] Username")
                print("[2] Password")
                print("[3] Remove them")
                sel = input()
                try:
                    sel = int(sel)
                    if sel in [1,2,3]:
                        break
                    else:
                        print("I didn't Understand")
                except ValueError:
                    print("I didn't Understand")
            if sel == 1:
                new = input("What would you like their new Username to be? ")
                admins.loc[admins["login"].str.lower() == user.lower(),"login"] = new
            if sel == 2:
                new = input("What would you like their new Password to be? ")
                admins.loc[admins["login"].str.lower() == user.lower(),"password"] = new
            if sel == 3:
                while True:
                    print("Are you sure you want to delete this User?")
                    print("[1] YES CANNOT BE UNDONE")
                    print("[2] NO")
                    sure = input()
                    try:
                        sure = int(sure)
                        if sure in [1,2]:
                            break
                        else:
                            print("I didn't Understand")
                    except ValueError:
                        print("I didn't Understand")
                if sure == 1:
                    admins.drop(admins[users["login"].str.lower() == user.lower()].index,inplace=True)
                if sure == 2:
                    manage_admins(admin)
        else:
            print("I didn't Understand")
            manage_admins(admin)

def updateTrackers(user):
    user_id = users[users["login"]==user]['user_id']
    while True:
        print("Would you like to: ")
        print("[1] Change existing trackers")
        print("[2] Add a new tracker")
        sel = input()
        try:
            sel = int(sel)
            if sel in [1,2]:
                break
            else:
                print("I Didn't Understand")
        except ValueError:
            print("I Didn't Understand")
    if sel == 1:
        movie_progress = pd.merge(left=progress,right=movies,left_on='movie_id',right_on='id')
        tracker_list = movie_progress[movie_progress['user_id'] == user_id, 'original_title'].to_list()
        for each in tracker_list:
            print(each)
    if sel == 2:
        movie_list = cli_search()
        print("Which movie would you like to add?")
        print(movie_list)
        
updateTrackers()     
    
