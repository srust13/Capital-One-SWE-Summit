from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import parseParkNamesAndStates, getInfo,  parseDates, timeNeeded, getParkPicsURL, parseLatLong

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
'''
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
'''
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

# Main search page with menus to select from a list of parks or states
@app.route("/search", methods=["GET","POST"])
def search():
    parksDict = parseParkNamesAndStates()[0]
    statesDict = parseParkNamesAndStates()[1]
    # Get the full names of the states
    states = statesDict.keys()
    # Get the full names of the parks
    parks = parksDict.keys()
    
    # If the user reached the link by submitting the form, or by using a parkCode in the URL (other pages in the program submit parkCode to URL)
    if request.method == "POST" or request.args.get("parkCode"):
        park = request.form.get("park") 
        parkCode = request.args.get("parkCode")
        
        #Store the full name of the state
        fullStateName = request.form.get("state")        

        # If the user selected a park from the drop down, render park.html, else render state.html
        if park or parkCode:
           
            # Keep track of if the park is valid. assume park is valid if user is selecting from drop down menu but not from URL            
            validPark = False
            
            # Define both park and parkCode and get their latitude and longitudes. continue with the code if validPark is True (will only be True if the parkCodes match)
            if park:
                parkCode = parksDict[park]
            
            aboutParksList = getInfo("parks",parkCode,"","", "entranceFees")
            if aboutParksList:
                for parkItem in aboutParksList:
                    if parkCode == parkItem.get("parkCode"):
                        # park=parkItem.get("fullName") is not the most effective call since the NPS API has HTML embedded for park names
                        # such as "Haleakal&#257; National Park" (see README). Instead get the park name from the dict which parses list of names from NPS official site using Beautiful Soup
                        for counter, parkCodeValue in enumerate(parksDict.values()):
                            if parkCode == parkCodeValue:
                                park = list(parksDict.keys())[counter]
                        lat_long = parseLatLong(parkItem.get("latLong", "")) 
                        validPark = True            

            # Get all necessary information if the park entered is valid. Else, redirect the user back to the search page so they can make another search request
            if validPark:
                parkPicsURL = getParkPicsURL(parkCode)
                visitorCentersList = getInfo("visitorCenters", parkCode, "", "", "") 
                campgroundsList = getInfo("campgrounds", parkCode,"", "", "")
                alertsList = getInfo("alerts", parkCode,"", "", "")
                articlesList = getInfo("articles",parkCode, "", "", "")             

                eventsList = getInfo("events", parkCode,"", "", "") 
                dates = []
                duration = []
                
                # Get information of when events are happening and their times
                for event in eventsList:
                    dates.append(parseDates(event.get("recurrencerule",""), event.get("datestart","")))
                    eventTime = event.get("times")
                    if eventTime:
                        eventTime = eventTime[0]
                        duration.append(timeNeeded(eventTime.get("timestart"), eventTime.get("timeend")))
                    
                newsList = getInfo("newsreleases", parkCode,"", "", "")
                lessonsList = getInfo("lessonplans",parkCode, "", "", "")
                peopleList = getInfo("people", parkCode,"", "", "")
                placesList = getInfo("places", parkCode,"", "", "")

                return render_template("park.html",park=park, parkPicsURL=parkPicsURL, aboutParksList=aboutParksList, lat_long=lat_long, visitorCentersList=visitorCentersList, 
                    campgroundsList=campgroundsList, alertsList=alertsList, articlesList=articlesList, eventsList=eventsList, dates=dates, 
                    duration=duration, newsList=newsList, lessonsList=lessonsList, peopleList=peopleList, placesList=placesList)
            
            else:
                flash("This park does not exist. Please select another park.")
                return redirect("/search")
        
        elif fullStateName:
            state = statesDict[fullStateName]
            parkPicsURL = {}
            parksURL = {}
            aboutParksList = getInfo("parks", "",state,"", "entranceFees")

            if aboutParksList:
                # Generate a list of parks that are in the same state as the state selected
                stateParksList = [park for park in aboutParksList if park.get("states").index(state)>=0]            
                
                # Get the images for the parks and store the URL that will be used in the anchor tags in the HTML for the park in a dict. Get the image from
                # the API since it can be scaled into a square better, otherwise use the one parsed from NPS site. If both don't exist, use stock image
                for park in stateParksList:
                    myPark = park.get("parkCode")
                    try:
                        try:
                            parkPicsURL[myPark] = getParkPicsURL(myPark)[1]
                        except:
                            parkPicsURL[myPark] = getParkPicsURL(myPark)[0]
                    except:
                        parkPicsURL[myPark] = ""
                    # Attach the URL of each respective park in the list
                    parksURL[myPark] = "/search?parkCode="+myPark
                return render_template("state.html",fullStateName=fullStateName, stateParksList=stateParksList, parkPicsURL=parkPicsURL, parksURL=parksURL)
            else:
                flash("The search was taking too much time or there were no parks in the selected state. Please try again.")
                return redirect("/search")
    else:
        # If the user gets to the page with a GET request, such as by clicking a link, render the search menus
        return render_template("search.html",parks=parks,states=states)
  
# Search using a keyword as input
@app.route("/keyword-search", methods=["GET","POST"])
def keyword_search():
    if request.method == "POST":
        query = request.form.get("searchQuery") 
        parkPicsURL = {}
        parksURL = {}
        aboutParksList = getInfo("parks", "","",query, "entranceFees")        
        
        # If the National Park Service API responded with a non-empty JSON, get the images for the parks and store the URL that will be used in
        # the anchor tags in the HTML for the park in a dict. Otherwise redirect back to the page and notify the user that the request has no results
        if aboutParksList:
            for park in aboutParksList:
                myPark = park.get("parkCode")
                try:
                    try:
                        parkPicsURL[myPark] = getParkPicsURL(myPark)[1]
                    except:
                        parkPicsURL[myPark] = getParkPicsURL(myPark)[0]
                except:
                    parkPicsURL[myPark] = ""
                # Url of the respective park
                parksURL[myPark] = "/search?parkCode="+myPark
            return render_template("query.html", query=query, aboutParksList=aboutParksList, parkPicsURL=parkPicsURL, parksURL=parksURL) 
        else:
            flash("The search was taking too much time or there were no results found for your search. Please try again.")
            return redirect("/keyword-search")
    else:
        return render_template("keyword-search.html")

# Search by designation
@app.route("/designation-search", methods=["GET","POST"])
def designation_search():
    if request.method == "POST":
        designation = request.form.get("designation") 
        parkPicsURL = {}
        parksURL = {}
        designationParksList = []
        aboutParksList = getInfo("parks", "","", designation, "entranceFees")  
        
        # If the National Park Service API responded with a non-empty JSON, get a list of all the parks that match the designation selected by the user,
        # get the images for the parks and store the URL that will be used in the anchor tags in the HTML for the park in a dict. Otherwise redirect 
        # back to the page and notify the user that the request has no results
        if aboutParksList:
            for park in aboutParksList:
                if designation == park.get("designation"):
                    designationParksList.append(park)
                    myPark=park.get("parkCode")
                    try:
                        try:
                            parkPicsURL[myPark] = getParkPicsURL(myPark)[1]
                        except:
                            parkPicsURL[myPark] = getParkPicsURL(myPark)[0]
                    except:
                        parkPicsURL[myPark] = ""
                    # Url of the respective park
                    parksURL[myPark] = "/search?parkCode="+myPark
            return render_template("designations.html", designation=designation, designationParksList=designationParksList, parkPicsURL=parkPicsURL, parksURL=parksURL) 
        else:
            flash("The search was taking too much time or there were no parks that fit the selected designation. Please try again.")
            return redirect("/designation-search")
    else:
        return render_template("designation-search.html")


# Jinja custom template filter to format value in currency
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    if "${:,.2f}".format(value) == "0.00":
        return "Free"
    else:
        return "${:,.2f}".format(value)