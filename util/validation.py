import sqlite3

db = sqlite3.connect("YALE_BRUDDER")
c = db.cursor()

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

