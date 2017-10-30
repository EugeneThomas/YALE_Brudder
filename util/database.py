import datetime
import sqlite3

db = sqlite3.connect("YALE_BRUDDER")
c = db.cursor()


def initialize_tables():
    command = '''
    CREATE TABLE accounts(
        username TEXT PRIMARY KEY,
        password TEXT
    );
    '''
    c.execute(command)
    command = '''
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
def new_post(username, title, content,logged_in):
    if(logged_in):
        timestamp = timestamp()
        command = 'INSERT INTO blog VALUES("{0}", "{1}", "{2}", "{3}")'.format(username,title,content,timestamp)
        c.execute(command)
    else:
        redirect(url_for(login))

#to retrieve all posts from a user
def get_post(username):
    command = 'SELECT * FROM  blog where name = "{0}";'.format(username)
    return c.execute(command)

#to retrieve all post titles and username
def get_all_post():
    command = "SELECT post_title, blog.name FROM blog;"
    return c.execute(command)

#to add new accounts
def new_acc( username, password):
    command = "SELECT username FROM accounts;".format(username)
    existing_usernames = c.execute(command)
    for existing_username in existing_usernames:
        if existing_username == username:
            print "duplicate username:"
            print existing_username
            return "That username has been taken!"
    command = 'INSERT INTO accounts VALUES("{0}", "{1}");'.format( username, password);
    c.execute(command)
    
    
#to authenticate username password commbination
def acc_auth(username, password):
    command = 'SELECT username FROM accounts WHERE username="{0}";'.format(username)
    valid_usernames = c.execute(command)
    for account in valid_usernames:
        command = 'SELECT username, password FROM accounts WHERE username="{0}" AND password ="{1}";'.format(username, password)
        valid_accounts = c.execute(command)
        for account in valid_accounts:
            return "successful login"
        return "wrong password"
    return "wrong username"

initialize_tables()
new_acc("Leo","hehexd")
print acc_auth("Leo","hehexd")
print acc_auth("Leo","whatevs")
print acc_auth("not Leo", "hmmmm")

db.commit()
db.close()
