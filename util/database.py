import datetime
import sqlite3


db = sqlite3.connect("YALE_BRUDDER")



def initialize_tables():
    c = db.cursor()
    command = '''
    CREATE TABLE accounts(
        username TEXT PRIMARY KEY,
        password TEXT
    );
    '''
    c.execute(command)
    c.close()
    c = db.cursor()
    command = '''
    CREATE TABLE blog(
        name TEXT,
        post_title TEXT,
        post_content TEXT
    );
    '''
    c.execute(command)
    c.close()

#to make a new post
def new_post(username, title, content):
    c = db.cursor()
    command = 'INSERT INTO blog VALUES("{0}", "{1}", "{2}")'.format(username,title,content)
    c.execute(command)
    c.close()


#to retrieve all posts from a user
def get_post(username):
    c = db.cursor()
    command = 'SELECT * FROM  blog where name = "{0}";'.format(username)
    blog = c.execute(command)
    c.close()
    out_blog = []
    for post in blog:
        out_post = {}
        out_post["username"] = post[0]
        out_post["title"] = post[1]
        out_post["content"] = post[2]
        out_blog.append(out_post)
    print out_blog
    return out_blog

#to retrieve all post titles and username
def get_all_post():
    c = db.cursor()
    command = "SELECT * FROM blog;"
    blog = c.execute(command)
    c.close()
    out_blog = []
    for post in blog:
        out_post = {}
        out_post["username"] = post[0]
        out_post["title"] = post[1]
        out_post["content"] = post[2]
        out_blog.append(out_post)
    print out_blog
    return out_blog


#to add new accounts
def new_acc(username, password):
    c = db.cursor()
    command = "SELECT username FROM accounts;".format(username)
    existing_usernames = c.execute(command)
    for existing_username in existing_usernames:
        if existing_username == username:
            print "duplicate username:"
            print existing_username
            c.close()
            return "That username has been taken!"
    c = db.cursor()
    command = 'INSERT INTO accounts VALUES("{0}", "{1}");'.format(username, password);
    c.execute(command)
    c.close()

#to authenticate username password commbination
def acc_auth(username, password):
    c = db.cursor()
    command = 'SELECT username FROM accounts WHERE username="{0}";'.format(username)
    valid_usernames = c.execute(command)
    c.close()
    for account in valid_usernames:
        c = db.cursor()
        command = 'SELECT username, password FROM accounts WHERE username="{0}" AND password ="{1}";'.format(username, password)
        valid_accounts = c.execute(command)
        c.close()
        for account in valid_accounts:
            return "successful login"
        return "wrong password"
    return "wrong username"


if __name__ == "__main__":
    initialize_tables()
    new_acc("Fluffy", "subject1")
    new_acc("Sluffy", "subject2")
    new_acc("Thluffy", "subject3")


if __name__ == "__main__":
    initialize_tables()
    new_acc("Fluffy", "subject1")
    new_acc("Sluffy", "subject2")
    new_acc("Thluffy", "subject3")
    print acc_auth("Duffy","subject4")
    print acc_auth("Fluffy","subject4")
    print acc_auth("Fluffy","subject1")
    new_post("Fluffy","Hi","HAI")
    new_post("Fluffy","Bye","BAI")
    new_post("Sluffy","Me","My name is Sluffy")
    print "Fluffy:"
    print get_post("Fluffy")
    print "Sluffy:"
    print get_post("Sluffy")
    print "Thluffy:"
    print get_post("Thluffy")
    print "All:"
    print get_all_post()


'''test cases not meant to be ran
new_acc("Leo","hehexd")
print acc_auth("Leo","hehexd")
print acc_auth("Leo","whatevs")
print acc_auth("not Leo", "hmmmm")
'''
db.commit()
db.close()
