import datetime
import sqlite3


db = sqlite3.connect("YALE_BRUDDER", check_same_thread=False)
c = db.cursor()


def initialize_tables():
    command = '''
    CREATE TABLE accounts(
        username TEXT PRIMARY KEY,
        password TEXT
    );
    '''
    db.commit()
    command = '''
    CREATE TABLE blog(
        name TEXT,
        post_title TEXT,
        post_content TEXT
    );
    '''
    c.execute(command)
    db.commit()

#to make a new post
def new_post(username, title, content):
    command = 'INSERT INTO blog VALUES("{0}", "{1}", "{2}")'.format(username,title,content)
    c.execute(command)
    db.commit()

#to edit title and content
def edit_post(username, old_title, new_title, new_content):
    command = 'UPDATE blog SET post_title = "{0}", post_content = "{1}" WHERE post_title = "{2}" AND name = "{3}"'.format(new_title, new_content, old_title, username)
    c.execute(command)
    db.commit()
    
#to retrieve all posts from a user
def get_post(username):
    command = 'SELECT * FROM  blog where name = "{0}";'.format(username)
    blog = c.execute(command)
    
    out_blog = []
    for post in blog:
        out_post = {}
        out_post["username"] = post[0]
        out_post["title"] = post[1]
        out_post["content"] = post[2]
        out_blog.append(out_post)
    #print out_blog
    return out_blog

#to retrieve all post titles and username
def get_all_post():
    command = "SELECT * FROM blog;"
    blog = c.execute(command)
    out_blog = []
    for post in blog:
        out_post = {}
        out_post["username"] = post[0]
        out_post["title"] = post[1]
        out_post["content"] = post[2]
        out_blog.append(out_post)
    #print out_blog
    return out_blog


#to add new accounts
def new_acc(username, password):
    command = "SELECT username FROM accounts WHERE username=={0};".format(username)
    existing_usernames = c.execute(command)
    for existing_username in existing_usernames:
        if existing_username == username:
            print "duplicate username:"
            print existing_username
            return "That username has been taken!"
    c.close()
    c = db.cursor()
    command = 'INSERT INTO accounts VALUES("{0}", "{1}");'.format(username, password);
    db.commit()

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



'''
if __name__ == "__main__":
    initialize_tables()
    new_acc("Fluffy", "subject1")
    new_acc("Sluffy", "subject2")
    new_acc("Thluffy", "subject3")
'''

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
    print "editing Fluffy's Hi post..."
    edit_post("Fluffy","Hi","Hello","Whats up")
    print "Fluffy:"
    print get_post("Fluffy")
    print "All:"
    print get_all_post()


'''test cases not meant to be ran
new_acc("Leo","hehexd")
print acc_auth("Leo","hehexd")
print acc_auth("Leo","whatevs")
print acc_auth("not Leo", "hmmmm")
'''
