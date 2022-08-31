import pandas as pd
from sqlalchemy import create_engine

sql = 'sqlite+pysqlite:///GroupProject2.db'
engine = create_engine(sql)

movies = pd.read_sql("SELECT * FROM movies",engine)
users = pd.read_sql("SELECT * FROM users",engine)
progress = pd.read_sql("SELECT * FROM progress",engine)

currentUser = None

def userLogin():
    success = False
    username = input("Username: ")
    password = input("Password: ")

    logins = users["login"].tolist()

    if username not in logins:
        print("Invalid username")
        return success
    else:
        if (users[users["login"] == username]["password"] != password):
            print("Password is incorrect")
            return success 
    
    global currentUser
    currentUser = username
    
    success = True
    return success

def navigateMenu(user):
    while True:
        print("User Options:")
        print("[1] View Trackers")
        print("[2] Update Trackers\n")

        selection = input("Which would you like to do? ")
        
        try:
            selection = int(selection)
        except ValueError:
            selection = input("Improper selection: Which would you like to do? ")

        if selection == 1:
            viewTrackers(user)
        elif selection == 2:
            updateTrackers(user)
        else:
            print("Invalid option. Please make a proper selection.")

def viewTrackers(user):
    while True:
        print("[1] Saved to Watch")
        print("[2] Currently Watching")
        print("[3] Finished Watching")
        input("Select which tracker you'd like to see:" )
        

def updateTrackers(user):
    pass


#user menu to update and view trackers
#I figured this can just be command line for now. GUI can come later

def agg_genre(row,genre):
    for each in row['genre']:
        if each['name'] == genre:
            return True
    return False

def search_movie(title = None,genre = None):
    if title:
        return movies[movies['title'] == title]
    if genre:
        return movies['genre'].apply(agg_genre, axis='columns',args=genre)
