import datetime
import sqlite3

db = sqlite3.connect("YALE_BRUDDAH")
c = db.cursor()

def initialize_tables():
    command = '''
    CREATE TABLE accounts(
        name TEXT,
        username TEXT,
        password TEXT,
        PRIMARY KEY( name, username)
    );
    CREATE TABLE blog(
        name TEXT,
        post_title TEXT,
        post_content TEXT,
        post_timestamp BLOB
    );
    '''
    # 2 primary keys!
    c.execute(command)

#to log timestamp:
def timestamp():
    return('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

def new_post(name, title, content):
    if(logged_in):
        command = 'INSERT INTO blog VALUES(%s, %s, %s, %s)'.format(name,title,content,timestamp())
    else:
        redirect(url_for(login))
