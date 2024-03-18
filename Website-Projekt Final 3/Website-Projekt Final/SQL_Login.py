import sqlite3
import sys
import os

def SQL_Query(Query, mycursor, conn):
    mycursor.execute(Query)
    conn.commit()

#username = sys.argv[1]
#password = sys.argv[2]

def CheckUsername(username, password):
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
        if(CheckPassword(username, password) == "Valid"):
            return "Registered"
        else:
            return "Wrong Password"


def CheckPassword(username, password):
    #configer cursor
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/databases/users.db")
    cur = conn.cursor()

    Query = f'SELECT password FROM user WHERE username == "{username}";'
    results = cur.execute(Query)

    for _ in results:
        realPassword = _
    
    #print(f"realPassword: {realPassword}, givenPassword: {password}")

    #close cursor
    cur.close()
    conn.close()

    #Change tuple to string to prepare for comparison
    realPassword = ''.join(realPassword)

    if(realPassword.strip("(),'") == password):
        return "Valid"
    elif(realPassword.strip("(),'") != password):
        return "Invalid"

def CheckIfValid(username, password):
    result = CheckUsername(username, password)
    if(result == "Not Registered"):
        return "Not Registered"
    elif(result == "Registered"):
        return "Registered"
    elif(result == "Wrong Password"):
        return "Wrong Password"

#cur.close()
#conn.close()