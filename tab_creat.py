import sqlite3
 
from sqlite3 import Error
 
def sql_connection():
 
    try:
 
        con = sqlite3.connect('planner.db')
 
        return con
 
    except Error:
 
        print(Error)
 
def sql_table(con):
 
    cursor = con.cursor()
 
    cursor.execute("CREATE TABLE planner(id integer unique PRIMARY KEY, user_id integer,plan text)")
 
    con.commit()
 
con = sql_connection()
sql_table(con)