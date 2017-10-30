

#lots to import
from flask import Flask, render_template, request, session, redirect, url_for, flash
import util.database as database
#import util.validation as validation
import os
app = Flask(__name__)
user1 = "username"
pass1 = "password"

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

@app.route("/register")
def register():
        user = request.args["user"]
        pass1 = request.args["pass"]
        pass2 = request.args["pass2"]
        if pass1 == pass2:
            if database.acc_auth(user,pass1) != False:
                flash('Account exists')
                return render_template("makeaccount.html")
            else:
                database.new_acc(user,pass1)
                flash("Account has been successfully made!")
                return redirect("/")
        else:
            flash("Passwords does not match")
            return render_template("makeaccount.html")

#woo will check to see the inputted username and password combination match the one on record
@app.route("/login", methods=["GET","POST"])
def verify():
    if "username" in session:
        username = session["username"]
        #return the greeting page if the user is logged in
        return redirect("loggedin")
    else:
        return render_template("login.html", username = user1, password = pass1)

    username = request.form["username"]
    password = request.form["password"]
    #checks if the form info matches the account info
    if(username == user1 and password == pass1):
        session["username"] = username
        flash('Correct information')
        #if both username and password match, show them the greet page
            #return render_template("greet.html", username= username)
        return redirect("/loggedin")

    #tell user their username is wrong if it does not match
    if(username != user1):
        flash('Wrong username!')
        return render_template("login.html")


    #tell user their password is wrong if it does not match
    if(password != pass1):
        flash('Wrong password!')
        return render_template("login.html")

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
@app.route("/makeaccount")
def makeaccount():
    #during verification, when you redirect to mistake you specify the error message and pass it over the url
    return render_template("makeaccount.html")



#necessary to run the app
if __name__ == "__main__":
    app.debug = True
    app.run()
