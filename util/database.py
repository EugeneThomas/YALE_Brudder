import datetime
import sqlite3

db = sqlite3.connect("YALE_BRUDDER")
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

#to make a new post
def new_post(name, title, content,logged_in):
    if(logged_in):
        command = 'INSERT INTO blog VALUES(%s, %s, %s, %s)'.format(name,title,content,timestamp())
    else:
        redirect(url_for(login))

#to retrieve all posts from a user
def get_post(name):
    command = "SELECT * FROM  blog;"
    return c.execute(command)

#to retrieve all post titles and username
def get_all_post():
    command = "SELECT post_title, blog.name FROM blog;"
    return c.execute(command)
    
def acc_auth(username, password):
    command = "SELECT username, password FROM accounts WHERE username=\""+username+"\", password =\""+password+"\";"
    if c.execute(command) == null:
        return False
    return True
