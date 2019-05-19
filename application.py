from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import listParksAndStates


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET","POST"])
def search():
    #parks=["Zion","Yellow"]
    #states=["hi"]
    parks=listParksAndStates()[0]
    states=listParksAndStates()[1]

    return render_template("search.html", parks, states)
    '''
    if request.method=="POST":
        return render_template("search.html") 
    else:
        return render_template("search.html")
        '''
  
@app.route("/advanced-search", methods=["GET","POST"])
def advanced_search():
    if request.method=="POST":
        return render_template("advanced-search.html") 
    else:
        return render_template("advanced-search.html")

