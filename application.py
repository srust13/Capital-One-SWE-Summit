from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import listParksAndStates, getInfo
from random import randint

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
    parks=listParksAndStates()[0]
    states=listParksAndStates()[1]
    if request.method=="POST":
        park=request.form.get("park")
        state=request.form.get("state") 

        #If the user selected a park from the drop down, render park.html, else render state.html
        if park:     
            visitorCentersList=getInfo(park, "visitorCenters") 
            campgroundsList=getInfo(park, "campgrounds")
            alertsList=getInfo(park, "alerts")

            #Need to print out top 5 articles if there are more than 5 articles 
            articlesList=getInfo(park, "articles") 
            articlesList_length=len(articlesList)
            topArticles=5
            if articlesList_length >= topArticles:
                #Make sure random number is unique so same article doesn't show up
                random=[]
                random=[randint(0,articlesList_length-1) for i in range(0,topArticles) if randint(0,articlesList_length-1) not in random]

            return render_template("park.html",park=park, visitorCentersList=visitorCentersList, campgroundsList=campgroundsList, alertsList=alertsList, 
            articlesList=articlesList,articlesList_length=articlesList_length, random=random )
        else:
            return render_template("state.html",state=state)

    else:
        return render_template("search.html",parks=parks,states=states)
  
@app.route("/advanced-search", methods=["GET","POST"])
def advanced_search():
    if request.method=="POST":
        return render_template("advanced-search.html") 
    else:
        return render_template("advanced-search.html")