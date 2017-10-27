import sqlite3

db = sqlite3.connect("YALE_BRUDDER")
c = db.cursor()

'''
def compare(username):
    command = "SELECT username FROM accounts;"
    user_retrieve = c.execute(command)
    for row in user_retrieve:
        if row[0] = username:
            return True
    return False


def compare(password):
    command = "SELECT password FROM accounts;"
    user_retrieve = c.execute(command)
    for row in user_retrieve:
        if row[0] = password:
            return True
    return False       
'''

#validate credentials

def validate(username, password):
    '''
    Validate credentials
    
    Validate credentials and generate error message if necessary
    
    args:
    username (str): username of the account
    password (str): password of the account

    rets:
    ret_val[0] boolean, whether or not login was successful
    ret_val[1] string , if ret_val[0] is false, error message, else, the username
    '''
    command = "SELECT username FROM accounts WHERE username={0}".format(username)
    user_retrieved = c.execute(command)
    if (user_retrieved == None):
        return [False,"Invalid username"]
    command = "SELECT username FROM accounts WHERE usename={0}, password={1}".format(username, password)
    user_retrieved = c.execute(command)
    if (user_retrieved == None):
        return [False,"Wrong password"]
    return [True, username]
