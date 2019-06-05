import requests, json, html, os
from random import randint
from datetime import datetime
from bs4 import BeautifulSoup


# Use Beautiful Soup to generate a list of all the park names and the states to be used in the search bar by parsing the HTML from the NPS site (explained in README)
def parseParkNamesAndStates():
    # Both dicts defined as key:value -> name:code
    parks={}
    states={}
    parkPicURL="https://www.nps.gov/findapark/advanced-search.htm"
    response=requests.get(parkPicURL)
    soup=BeautifulSoup(response.text, "html.parser")
    
    optionParks = soup.find("select",{"name":"alphacode"}).findAll("option")
    optionStates = soup.find("select",{"id":"form-park"}).findAll("option")
    
    # Convert all items of the Soup object to a string and unescape any HTML characters to keep original text
    parksStrings=[html.unescape(str(park)) for park in optionParks]
    statesStrings=[html.unescape(str(state)) for state in optionStates]    

    # Get the parkName:parkCode from the HTML option and append in dict. All parkCodes are in format ' "aaaa"> ' and all parks are in format ' >bbbb</ ' 
    for park in parksStrings:
        parkCode = park[park.index("\"")+1 : park.index("\">")]
        parkName= park[park.index(">")+1:park.index("</")]
        parks[parkName]=parkCode
    
    # "state" is first item because of the way it is in the search bar in the HTML. Need to remove it
    del statesStrings[0]
    
    #Append state:stateCode to dict. All state codes are of length 2. All states are in format ' >aaaa</ '
    for state in statesStrings:
        baseIdx=state.index("\"")+1
        stateCode = state[baseIdx : baseIdx+2]
        stateName = state[state.index(">")+1:state.index("</")]
        states[stateName] = stateCode
    return parks,states

# Make a call to the API to get relevant information. infoType can equal "parks", visitorCenters", "alerts", etc
def getInfo(infoType, parkCode, stateCode, parkName, fields):    
    url="https://developer.nps.gov/api/v1"
    api= os.environ['NPS_API_KEY']
    results=[]
    
    #Try requesting. If it fails, return an empty array
    try:
        endpoint = requests.get(f"{url}/{infoType}?parkCode={parkCode}&stateCode={stateCode}&q={parkName}&fields={fields}&api_key={api}")
        data = endpoint.json() 

        #if a park code is provided, make sure each item in the JSON response matches the park code. Matching by parkCode was chosen instead of by full name (see README)
        if parkCode:
            for item in data["data"]:
                
                #if the item provides a parkCode, make sure it matches with input. If it doesn't have a parkCode at all (some don't), then append it regardless. 
                # If the item has a parkCode and it doesn't match, then don't add
                if item.get("parkCode",""):
                    if item.get("parkCode")==parkCode:
                        results.append(item)
                else:
                    results.append(item)
            return results
        else:
            return data["data"]
    except:
        return []
        

# Use Beautiful Soup to get the link of the first image associated with a park (makes for a nice hero picture) and then gets the other images from API request
def getParkPicsURL(parkCode):
    images=[]
    parks=getInfo("parks", parkCode,"", "", "images")
    
    for park in parks: 
        parkPicURL="https://www.nps.gov/" +parkCode +"/index.htm"
        response=requests.get(parkPicURL)
        soup=BeautifulSoup(response.text, "html.parser")
        image = soup.find("meta",  property="og:image")
        if image:
            images.append(image["content"])

        for image in park.get("images"):
            images.append(image.get("url"))
    return images

# Parse the recurrence rule code  
def parseDates(rec, startDate):
    rrule=[]
    months={"01":"January", "02": "February", "03": "March", "04": "April","05":"May","06": "June", 
        "07":"July","08":"August","09":"September","10":"October","11":"November", "12":"December"}        
    
    if rec!="":
        
        # Get the start and end date of the event. year of length 4, month of length 2, and day of length 2
        for i in range(0,2):
            baseIdx = rec.index("=")
            year=rec[baseIdx + 1 : baseIdx + 5]
            month=months[rec[baseIdx + 5 : baseIdx + 7]]
            day=rec[baseIdx + 7 : baseIdx + 9]
            rrule.append(month+" "+day+", "+year)
            rec=rec[baseIdx + 9::]
        
        days={"MO":"Monday", "TU":"Tuesday", "WE":"Wednesday", "TH":"Thursday", "FR":"Friday", "SA":"Saturday", "SU":"Sunday"}
        
        # If event recurs every single day, just append "day" ("every" will be the in html regardless)
        try:
            rec.index("FREQ=DAILY")            
            rrule.append("day")
        except:
            
            # Gets the list of recurring days. "byday=" has length 6
            rec=rec[rec.index("BYDAY")+6::]
            rec=rec[0:rec.index(";")]    
            daysList=rec.split(",")
            
            # Append the day with a "," if it is not the last day in the list, otherwise just append the day to the list
            for i, day in enumerate(daysList):
                if i<len(daysList)-1:
                    rrule.append(days[str(day)]+", ")    
                else:
                    rrule.append(days[str(day)])
        
    # If there is no reccurence rule, the event is a one day event. Convert to date
    if rec=="" and startDate!="":
        startBaseIdx=startDate.index("-")
        startYear=startDate[0:startBaseIdx]
        startMonth=months[startDate[startBaseIdx+1:startBaseIdx+3]]
        startDay=startDate[startBaseIdx+5:startBaseIdx+7]
        date=startMonth+" "+startDay+", "+startYear
        rrule.append(date)

        # Append the corresponding day of a given date
        rrule.append(datetime.strptime(date, '%B %d, %Y').strftime('%A'))
    return rrule

# Given two times, get the duration in between them
def timeNeeded(startTime, endTime):
    tdelta="Not available"
    if startTime=="" or endTime=="":
        return tdelta
    startTime=startTime.replace(" ", ":")
    endTime=endTime.replace(" ", ":")
    FMT = '%I:%M:%p'
    tdelta = datetime.strptime(endTime, FMT) - datetime.strptime(startTime, FMT) 
    seconds = tdelta.total_seconds()
    hours = int(seconds // 3600)    
    minutes = int((seconds % 3600) // 60)
    if hours>0 and minutes>0:
        return str(hours)+" hours and "+str(minutes)+ " minutes" 
    elif hours==0 and minutes>0:
        return str(minutes)+ " minutes" 
    else:
        return str(hours)+ " hours"


# Parse the API response: "latLong": "lat:61.4182147, long:-142.6028439" and return the latitude and longitude strings
def parseLatLong(geocode):
    geocodes=[]
    if geocode=="":
        return geocodes
    latitude=geocode[geocode.index(":")+1 : geocode.index(",")]
    longitude=geocode[geocode.index("long:")+5:]
    geocodes=[latitude, longitude]    
    return geocodes

