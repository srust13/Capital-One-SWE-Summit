from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import listParksAndStates, getInfo,  parseRecurrence, timeNeeded


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
    if request.method=="POST" or request.args.get("park"):
        park=request.form.get("park") or request.args.get("park")
        state=request.form.get("state") 

        #If the user selected a park from the drop down, render park.html, else render state.html
        if park:     
            aboutParksList=getInfo(park,"parks")
            visitorCentersList=getInfo(park, "visitorCenters") 
            campgroundsList=getInfo(park, "campgrounds")
            alertsList=getInfo(park, "alerts")
            articlesList=getInfo(park, "articles")             

            eventsList=getInfo(park, "events") 
            topEvents=4
            dates=[]
            duration=[]
            for event in eventsList:
                dates.append(parseRecurrence(event.get("recurrencerule","")))
                eventTime= event.get("times")[0]
                duration.append(timeNeeded(eventTime.get("timestart"), eventTime.get("timeend")))
            
            newsList=getInfo(park, "newsreleases")
            lessonsList=getInfo(park, "lessonplans")
            peopleList=getInfo(park, "people")
            placesList=getInfo(park, "places")

            return render_template("park.html",park=park, aboutParksList=aboutParksList, visitorCentersList=visitorCentersList, 
            campgroundsList=campgroundsList, alertsList=alertsList, articlesList=articlesList, eventsList=eventsList, dates=dates, 
            duration=duration, newsList=newsList, lessonsList=lessonsList, peopleList=peopleList, placesList=placesList)
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