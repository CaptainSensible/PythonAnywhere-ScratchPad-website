
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="CaptainSensible",
    password="Magnus138!",
    hostname="CaptainSensible.mysql.pythonanywhere-services.com",
    databasename="CaptainSensible$Comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


# This is the function (tutorial is calling it a view) that controls what
# comes up when page is first launched.
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method =="GET":
        return render_template("index.html", comments=Comment.query.all())

    comment= Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect (url_for("index"))



#This is the function that controls the login screen.
#"GET", "POST" allow viewing (get) and submitted data (POST) of log in credentials.
@app.route("/login/", methods=["GET", "POST"])

#Below defines the function "login()" then says if just viewing the page (GET method)
#show the login screen (also it creates a variable "error" and sets it to false.
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

#This says if the system recieves anything other than a "GET" method (i.e. a POST)
#check the username and password fields, if they dont equal (!=) "admin" and "secret"
#reload the login screen but set the "error" variable to True.
    if request.form["username"] != "admin" or request.form["password"] != "secret":
        return render_template("login_page.html", error=True)

#And this just says if teh username and password are correct, load the app (index.html)
    return redirect (url_for("index"))

