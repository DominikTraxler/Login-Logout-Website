import sqlite3
import sys
import os
from termcolor import colored

def SQL_Query(Query, mycursor, conn):
    mycursor.execute(Query)
    conn.commit()

def GetPostData_User(username):
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/databases/users.db")
    cur = conn.cursor()

    #Get Data from Posts
    Query = f'SELECT PostID, Heading, "Text", Author FROM post INNER JOIN user ON ID = Author WHERE user.username = "{username}";'
    results = cur.execute(Query)

    postnames = []
    posttexts = []

    for _ in results:
        postnames.append(_[1])
        posttexts.append(_[2])

    cur.close()
    conn.close()

    return postnames, posttexts

def GetPostData_All():
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/databases/users.db")
    cur = conn.cursor()

    #Get Data from Posts
    Query = f'SELECT PostID, Heading, "Text", Author FROM post'
    results = cur.execute(Query)

    postnames = []
    posttexts = []
    postauthorsID = []

    for _ in results:
        postnames.append(_[1])
        posttexts.append(_[2])
        postauthorsID.append(_[3])

    #change authorsID to name
    postauthors = []
    Query = f'SELECT username FROM user INNER JOIN post ON user.ID == post.author'
    results = cur.execute(Query)

    for variable in results:
        postauthors.append(variable[0])

    cur.close()
    conn.close()

    return postnames, posttexts, postauthors


def InsertPostData(heading, text, author):
    conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "/databases/users.db")
    cur = conn.cursor()

    print(colored("Starting to pass in values", "green"))

    print(heading, text, author)

    Query = f'SELECT ID FROM user WHERE username == "{author}";'
    results = cur.execute(Query)

    for _ in results:
        author_ID = _

    #print(author_ID[0])

    Query = f"INSERT INTO post(Heading, Text, Author) VALUES('{heading}', '{text}', '{author_ID[0]}');"

    SQL_Query(Query, cur, conn)

    print(colored("Passing in should be successful", "green"))

    cur.close()
    conn.close()