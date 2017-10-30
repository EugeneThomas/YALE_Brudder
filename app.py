

#lots to import
from flask import Flask, render_template, request, session, redirect, url_for, flash
import util.database as database
#import util.validation as validation
import os
app = Flask(__name__)
ACCOUNTS = {"Username": "Password"}
BLOGS = {}
#creates String of 26 random characters
app.secret_key = os.urandom(26)

#initial login page will render form if not logged in already, and will render a greeting otherwise
@app.route("/", methods=["GET","POST"])
def login():
    #initializes username
    username = ""
    #"username" is the key that would be in the session dictionary if the user is logged in after inputting data into the form
    if "username" in session:
        username = session["username"]
        #return the greeting page if the user is logged in
        return redirect("loggedin")
    #return the login page if they are not
    return render_template("landing.html")

@app.route("/redirection", methods=["GET","POST"])
def redirection():
    if request.method == 'POST':
        if request.form['submit'] == 'Login':
            return redirect("login")
        if request.form['submit'] == "Register":
            return redirect("makeaccount")

@app.route("/redirection2", methods=["GET","POST"])
def redirection2():
    if request.method == 'POST' and "username" in session:
        if request.form['submit'] == "Make New Blog":
            return render_template("newblog.html", username=session["username"])
        elif request.form['submit'] == "View and Edit Old Blogs":
            return render_template("oldblogs.html", username=session["username"], collection=makedict(BLOGS,  session["username"]))
        elif request.form['submit'] == "See Other Blogs":
            return render_template("blogs.html", username=session["username"], collection=makedict2(BLOGS, session["username"]))
        else:
            return redirect("/loggedout")

@app.route("/home", methods=["GET","POST"])
def home():
    if "username" in session:
        if request.method == 'POST':
            return render_template("home.html", username=session["username"])


@app.route("/editblog", methods=["GET","POST"])
def editblogs():
    if "username" in session:
        blog = request.form['blog']
        return render_template("editblogs.html", username=session["username"], oldpost=blog)

# Makes a dicitonary with all of your posts inside:
def makedict(d, user):
    if "username" in session:
        retd = {}
        for i in d:
            if i == session["username"]:
                x = len(d[i])
                while x > 0:
                    k = d[i][x-2]
                    v = d[i][x-1]
                    retd[k] = v
                    x = x - 2
        print "The ting goes..."
        print retd
        return retd

# Makes a dicitonary with all of your posts inside:
def makedict2(d, user):
    if "username" in session:
        retd = {}
        for i in d:
            if i != session["username"]:
                x = len(d[i])
                while x > 0: 
                    k = d[i][0]
                    k = k + " by " + i
                    v = d[i][1]
                    retd[k] = v
        print retd
        return retd


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        user = request.form["username"]
        pass1 = request.form["password"]
        pass2 = request.form["password2"]
        if pass1 == pass2:
        ##    if database.new_acc(user, pass1) == "That username has been taken!":
            if (user in ACCOUNTS):
                flash("That username has been taken!")
                return render_template("makeaccount.html")
            else:
                session["username"] = user
                ##database.new_acc(user,pass1)
                ACCOUNTS[user] = pass1
                print ACCOUNTS
                return render_template("home.html", username = user)
        else:
            print "we here"
            flash("Passwords do not match")
            return render_template("makeaccount.html")

#woo will check to see the inputted username and password combination match the one on record
@app.route("/login", methods=["GET","POST"])
def verify():
    if "username" in session:
        username = session["username"]
        #return the greeting page if the user is logged in
        return redirect("loggedin")
    else:
        return render_template("login.html")

@app.route("/auth", methods=["GET","POST"])
def auth():
    username = request.form["username"]
    password = request.form["password"]
    #checks if the form info matches the account info
    if(username in ACCOUNTS):
        if(password != ACCOUNTS[username]):
            flash('Wrong password!')
            return render_template("login.html")
        else:
            session["username"] = username
            return render_template("home.html", username=username)
    else:
        flash('Wrong username!')
        return render_template("login.html")

@app.route("/newblog", methods=["GET", "POST"])
def newblog():
    if "username" in session:
        blog = request.form["blog"]
        title = request.form["title"]
        if session["username"] not in BLOGS:
            d = []
            d.append(title)
            d.append(blog)
            session["username"]
            BLOGS[session["username"]] = d
        else:
            d = BLOGS[session["username"]]
            d.append(title)
            d.append(blog)
            BLOGS.pop(session["username"])
            BLOGS[session["username"]] = d
        print BLOGS
        return render_template("home.html", username=session["username"])


#Removes user from the session (if they were in it to begin with), and then tells them
@app.route("/loggedout", methods=["GET","POST"])
def youre_out():
    #removes the username saved from the session
    if "username" in session:
        session.pop("username")
        return "You have been successfully logged out. Go <a href='/'>back</a>"
    return "You were never logged in. Try signing in  <a href='/'>here</a>"

#displays the greeting page, which acknowledges the user is logged in if there is a username in the session
@app.route("/loggedin", methods=["GET","POST"])
def youre_in():
    username = session["username"]
    if "username" in session:
       	return render_template("home.html", username = username)
    else:
       	return redirect("/")

#Lets the user know they made a mistake
@app.route("/makeaccount", methods=["GET", "POST"])
def makeaccount():
    #during verification, when you redirect to mistake you specify the error message and pass it over the url
    return render_template("makeaccount.html")



#necessary to run the app
if __name__ == "__main__":
    app.debug = True
    app.run()
