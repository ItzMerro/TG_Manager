from flask import Flask, render_template, redirect, request
import requests
import json
import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get("token")
url='https://api.telegram.org/bot%s/getUpdates' % TOKEN
app = Flask(__name__)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_chat(conn, chat):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO chats(chat_id,title,chat_type)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, chat)
    conn.commit()
    return cur.lastrowid

def create_member_of(conn, member):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO member_of (user_id, chat_id, chat_title)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, member)
    conn.commit()
    return cur.lastrowid 

def create_user(conn, user):
    """
    Create a new user
    :param conn:
    :param user:
    :return:
    """

    sql = ''' INSERT INTO users(user_id,first_name,username)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid



def main():
    database = r"pythonsqlite.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        user_id INTEGER PRIMARY KEY,
                                        first_name TEXT,
                                        username TEXT NOT NULL UNIQUE
                                    ); """

    sql_create_chats_table = """CREATE TABLE IF NOT EXISTS chats (
                                    chat_id INT PRIMARY KEY,
                                    title TEXT,
                                    chat_type TEXT 
                                );"""
    sql_create_member_of_table = """ CREATE TABLE IF NOT EXISTS member_of (
                                        user_id INTEGER NOT NULL,
                                        chat_id INTEGER NOT NULL,
                                        chat_title,
                                        FOREIGN KEY (user_id) REFERENCES users (user_id),
                                        FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
                                    );"""
    # create a database connection
    conn = create_connection(database) 
        
    
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)

        # create tasks table
        create_table(conn, sql_create_chats_table)

        # create tasks table
        create_table(conn, sql_create_member_of_table)
    else:
            print("Error! cannot create the database connection.")    

    with conn:
        response=requests.get(url)
        info = json.loads(response.text)
        user = []
        chat=[]
        for i in range(len(info['result'])):
            if 'new_chat_participant' in info['result'][i]['message']:
                counter = 0
                user.append(info['result'][i]['message']['new_chat_participant'])
                chat.append(info['result'][i]['message']['chat'])
                user_id = user[counter]['id']
                user_fname = user[counter]['first_name']
                username = user[counter]['username']

                chat_id = chat[counter]['id']
                chat_title = chat[counter]['title']
                chat_type = chat[counter]['type']


                # get user info
                add_user = (user_id, user_fname, username)
                # get chat info
                add_chat = (chat_id, chat_title, chat_type)
                member_of = (user_id, chat_id, chat_title)

                # add users to db
                try:
                    create_user(conn, add_user)
                    create_member_of(conn, member_of)
                    create_chat(conn, add_chat)
                except Error:
                    print('Error')
                # add chats to db
                
                # add member of 
                
                counter+=1


@app.route('/')
def home():

    # this should be fetched from the db now
    response=requests.get(url)
    info = json.loads(response.text)
    new_chat_member = []
    messages=[]
    for i in range(len(info['result'])):
        # messages.append(info['result'][i]['message']) 
        if 'new_chat_participant' in info['result'][i]['message']: 
            messages.append(info['result'][i]['message']['new_chat_participant'])
    
    return render_template("index.html", data=messages)


if __name__=='__main__':
    main()
    app.run(debug=True)


