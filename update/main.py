import pandas as pd
from sqlalchemy import create_engine

sql = 'sqlite+pysqlite:///GroupProject2.db'
engine = create_engine(sql)

movies = pd.read_sql("SELECT * FROM movies",engine,index_col="index")
users = pd.read_sql("SELECT * FROM users",engine,index_col="index")
progress = pd.read_sql("SELECT * FROM progress",engine,index_col='index')
admins = pd.read_sql("SELECT * FROM admins",engine,index_col='index')

def userLogin():
    success = False
    username = input("Username: ")
    password = input("Password: ")

    if users[users['login'] == username].empty:
        print("Invalid username")
        return success
    else:
        #print(users.loc[users["login"] == username, "password"].item())
        if (users.loc[users["login"] == username, "password"].item() == password):
            user_id = users[users['login'] == username]["user_id"].values
            navigateMenu(user_id[0])       
            return success
        else:
            print("Password is incorrect")
            return success
    main()

def navigateMenu(user):
    while True:
        print("User Options:")
        print("[1] View Trackers")
        print("[2] Update Trackers\n")
        print("[3] Exit")

        selection = input("Which would you like to do? ")
        
        try:
            selection = int(selection)
        except ValueError:
            selection = input("Improper selection: Which would you like to do? ")

        if selection == 1:
            viewTrackers(user)
        elif selection == 2:
            updateTrackers(user)
        elif selection == 3:
            print ("Have a nice day")
            return
        else:
            print("Invalid option. Please make a proper selection.")

def viewTrackers(user):
    #print(user)
    movie_progress = pd.merge(left=progress,right=movies, on='movie_id')
    #movie_progress.reset_index(inplace=True)
    #print(progress)
    #print(movie_progress)
    while True:
        print("[1] Saved to Watch")
        print("[2] Currently Watching")
        print("[3] Finished Watching")
        pick = input("Which do you want to see? ")
    
        try:
            pick =int(pick)
            if pick in [1,2,3]:
                break
        except ValueError:
            pick = input("Please pick an option from 1-3")
    
    if pick == 1:
        #planning to watch
        plan_watch = movie_progress[(movie_progress['user_id']==user) & (movie_progress['status']==1)].values
        for each in plan_watch:
            #print(each)
            cli_progress_bar(each[3])
            print(each[5])
    if pick == 2:
        #currently watching
        plan_watch = movie_progress[(movie_progress['user_id']==user) & (movie_progress['status']==2)].values
        #print(plan_watch)
        for each in plan_watch:
            cli_progress_bar(each[3])
            print(each[5])
    if pick == 3:
        #finished watching
        plan_watch = movie_progress[(movie_progress['user_id']==user) & (movie_progress['status']==3)].values
        for each in plan_watch:
            cli_progress_bar(each[3])
            print(each[5])
    
def updateTrackers(user):
    movie_progress = pd.merge(left=progress,right=movies, on='movie_id')
    while True:
        print("Would you like:")
        print("[1] Add new trackers")
        print("[2] Update existing trackers")
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
        options = cli_search()
        while True:
            for i in range(len(options)):
                #print(options)
                print(f"[{i}",end="]")
                print(options[i][2])
            movie = input("Which Movie would you like to add? ")
            try:
                movie = int(movie)
                if movie in range(len(options)):
                    break
                else:
                    print("I didn't Understand")
            except ValueError:
                print("I Didn't Understand")
        movie_id = options[movie][0]
        while True:
            print("Are you:")
            print("[1] Planning on watching")
            print("[2] Currently watching")
            print("[3] Finished watching")
            selec = input()
            try:
                selec = int(selec)
                if selec in [1,2,3]:
                    break
                else:
                    print("I Didn't Understand")
            except ValueError:
                print("I Didn't Understand")
        if selec == 1:
            progress.loc[len(progress.index)] = [user,movie_id,1,0]
        if selec == 2:
            while True:
                prog = input("What is the percentage you have watched? ")
                try:
                    prog = int(prog)
                    if prog < 100:
                        break
                    else:
                        print("I Didn't Understand")
                except ValueError:
                    print("I Didn't Understand")
            progress.loc[len(progress.index)] = [user,movie_id,2,prog]
        if selec == 3:
            progress.loc[len(progress.index)] = [user,movie_id,3,100]
    if sel == 2:
        option = movie_progress[movie_progress['user_id']==user].values
        while True:
            for i in range(len(option)):
                #print(options)
                print(f"[{i}",end="]")
                print(option[i][5])
            inp = input("Which would you like to change? ")
            try:
                inp = int(inp)
                if inp in range(len(option)):
                    break
                else:
                    print("I Didn't Understand")
            except ValueError:
                print("I Didn't Understand")
        while True:
            print("Would you like to: ")
            print("[1] Remove the tracker")
            print("[2] Change the progress of tracker")
            print("[3] Change the status of tracker")
            inpu = input()
            try:
                inpu = int(inpu)
                if inpu in [1,2,3]:
                    break
                else:
                    print("I Didn't Understand")
            except ValueError:
                print("I Didn't Understand")
        if inpu == 1:
            while True:
                print("Are you sure you want to delete this tracker?")
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
                print(progress[(progress['user_id'] == option[inp][0])&(progress['movie_id']==option[inp][1])].index)
                progress.drop(progress[(progress['user_id'] == option[inp][0])&(progress['movie_id']==option[inp][1])].index,inplace=True)
        if inpu == 2:
            while True:
                new_per = input("What is the new percentage? ")
                try:
                    new_per = int(new_per)
                    if new_per < 100:
                        break
                    else:
                        print("I didn't Understand")
                except ValueError:
                    print("I didn't Understand")
            progress.loc[(progress['user_id'] == option[inp][0])&(progress['movie_id']==option[inp][1]),'percent'] = new_per
        if inpu == 3:
            while True:
                print("Are you:")
                print("[1] Planning on watching")
                print("[2] Currently watching")
                print("[3] Finished watching")
                new_stat = input()
                try:
                    new_stat = int(new_stat)
                    if new_stat in [1,2,3]:
                        break
                    else:
                        print("I Didn't Understand")
                except ValueError:
                    print("I Didn't Understand")
            progress.loc[(progress['user_id'] == option[inp][0])&(progress['movie_id']==option[inp][1]),'status'] = new_stat

def search_movie(title = None,genre = None):
    if title:
        results = movies.loc[movies['original_title'].str.contains(title, case=False)]
        if not results.empty:
            return results.values
        else:
            print("Movie Not Found")
            cli_search()
    if genre:
        results = movies.loc[movies['genres'].str.contains(genre, case=False)]
        if not results.empty:
            return results.values
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

def cli_progress_bar(percent:int):
    length = int(percent/10)
    print("[",end="")
    for i in range(10):
        if i<length:
            print(u'\u2588',end=u'\u2588')
        else:
            print(" ", end=" ")
    print("]",end =" ")

def create_account():
    while True:
        user = input("Please enter Username: ")
        if users[users["login"].str.lower() == user.lower()].empty:
            password = input("Please enter password: ")
            print(users)
            users.loc[len(users.index)] = [len(users.index),user,password]
            break
        else:
            print(f"The user {user} already exists")
    main()

def write_sql():
    users.to_sql("users",engine,if_exists='replace')
    progress.to_sql("progress",engine,if_exists='replace')
    admins.to_sql("admins",engine,if_exists='replace')
    print("The program has exited successfully")
    
def create_admin():
    while True:
        user = input("Please enter Admin Username: ")
        if admins[admins["login"].str.lower() == user.lower()].empty:
            password = input("Please Admin enter password: ")
            print(len(users.index)+1)
            admins.loc[len(users.index)] = [len(users.index)+1,user,password]
            break
        else:
            print(f"The Admin {user} already exists")
    main()

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
        while True:
            print("Which user do you want to change?")
            user_list = users["login"].to_list()
            for i in range(len(user_list)):
                print(f"[{i}",end="]")
                print(user_list[i])
            user_choice = input()
            try:
                user_choice = int(user_choice)
                if user_choice in range(0,len(user_list)):
                    break
                else:
                    print("I Didn't Understand")
            except ValueError:
                print("I Didn't Understand")
        user = user_list[user_choice]
        if not users[users["login"] == user].empty:
            selected_user = users[users["login"] == user]
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
                navigateMenu(user)
                pass 
        else:
            print("I didn't Understand")
            manage_users(admin)
        main()

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
        main()

#=======Main Loop==============
def main():
    #forces the sql write
    try:
        print("Welcome to the movie tracker!")
        while True:
            print("Would you like to:")
            print("[1] Login as user")
            print("[2] Login as admin")
            print("[3] Create an account")
            print("[4] Exit")
            sel = input()
            try:
                sel = int(sel)
                if sel in [1,2,3,4]:
                    break
                else:
                    print("I Didn't Understand")
            except ValueError:
                print("I Didn't Understand")
        if sel == 1:
            #login user
            userLogin()
        if sel == 2:
            #login admin
            cli_admin()
        if sel == 3:
            #create user
            create_account()
        if sel == 4:
            pass
    finally:
        write_sql()


if __name__ == '__main__':
    main()
