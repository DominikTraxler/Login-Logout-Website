import sqlite3
import sys
import os
from termcolor import colored

def SQL_Query(Query, mycursor, conn):
    mycursor.execute(Query)
    conn.commit()

def CheckUsername(username):
    #configer cursor
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/databases/users.db")
    cur = conn.cursor()

    Query = f'SELECT ID FROM user WHERE username == "{username}";'
    results = cur.execute(Query)
    searchedID = -1
    for _ in results:
        searchedID = _
    
    #close cursor
    cur.close()
    conn.close()

    if(searchedID == -1):
        return "Not Registered"
    else:
        return "Registered"
    
def InsertAccountData(username, password, yob):
    #print("YUUUUUUUP" +  os.path.dirname(os.path.abspath(__file__)) + "/databases/users.db")
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/databases/users.db")
    cur = conn.cursor()

    print(colored("Starting to pass in values", "green"))

    print(username, password, yob)

    Query = f"INSERT INTO user(username, password, yob) VALUES('{username}', '{password}', '{yob}');"

    SQL_Query(Query, cur, conn)

    print(colored("Passing in should be successful", "green"))

    cur.close()
    conn.close()