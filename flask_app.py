
#This all comes from https://blog.pythonanywhere.com/121/ and part 2 of this tutorial

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
# Imports Flask-Login, a framework for loging in configuration.
# for info on this "Flask-Login" extension check below tutorial (about 1/6 down page) starts with "Doing something with login and logout"
#https://blog.pythonanywhere.com/158/
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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
migrate = Migrate(app, db)

app.secret_key = "1234567890qwertyuiop" #These 3 lines deal with "Flask-Login.
login_manager = LoginManager()
login_manager.init_app(app)

#The "User" class defined below has to do with the Flask-Login stuff.
class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

all_users = {
    "admin": User("admin", generate_password_hash("secret")),
    "bob" : User("bob", generate_password_hash("less-secret")),
    "caroline" : User("caroline", generate_password_hash("completely-secret")),
    }

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


# This is the function (tutorial is calling it a view) that controls what
# comes up when page is first launched.
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method =="GET":
        return render_template("index.html", comments=Comment.query.all()
        , timestamp=datetime.now())

    if not current_user.is_authenticated:
        return redirect(url_for("index"))

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

    username = request.form["username"]
    if username not in all_users:
        return render_template("login_page.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

#And this just says if the username and password are correct, load the app (index.html)
    login_user(user)
    return redirect (url_for("index"))

