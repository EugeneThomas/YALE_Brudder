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
        command = 'INSERT INTO blog VALUES({0}, {1}, {2}, {3})'.format(name,title,content,timestamp())
        c.execute(command)
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

#to add new accounts
def new_acc(displayed_name, username, password):
    command = "SELECT user FROM accounts WHERE user={0};".format(displayed_name)
    duplicate_name = c.execute(command)
    command = "SELECT username FROM accounts WHERE username={0};".format(username)
    duplicate_username = c.execute(command)
    if(duplicate_name != None):
        return "That name has been taken!"
    if(duplicate_username != None):
        return "That username has been taken!"
    command = "INSERT INTO accounts VALUES({0},{1},{2});".format(displayed_name, username, password);
    c.execute(command)
    
    
#to authenticate username password commbination
def acc_auth(username, password):
    command = 'SELECT username, password FROM accounts WHERE username="{0}", password ="{1}";'.format(username, password)
    if c.execute(command) == None:
        return False
    return True

c.commit()
c.close()
