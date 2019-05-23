from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import listParksAndStates, getInfo, generateRandom


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
            randomArticles=generateRandom(articlesList_length, topArticles)

            #Need to print out top 5 events if there are more than 5 events
            eventsList=getInfo(park, "events") 
            eventsList_length=len(eventsList)            
            topEvents=3
            randomNews=generateRandom(eventsList_length, topEvents)

            #Need to print out top 5 news releases if there are more than 5 news releases
            newsList=getInfo(park, "newsreleases") 
            newsList_length=len(newsList)            
            topNews=5
            randomNews=generateRandom(newsList_length, topNews)

            
            

            return render_template("park.html",park=park, visitorCentersList=visitorCentersList, campgroundsList=campgroundsList, alertsList=alertsList, 
            articlesList=articlesList,articlesList_length=articlesList_length, randomArticles=randomArticles,
            newsList=newsList, newsList_length=newsList_length, randomNews=randomNews )
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