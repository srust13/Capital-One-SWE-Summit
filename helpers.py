import requests, json
from random import randint
from datetime import datetime

url="https://developer.nps.gov/api/v1"
api= "nMeJTZeHbgdfQeRtllNPQImS4eP37B83Iu7Mt1Fe"

#Generate a list of all the park names in a given state
def listParksByState(stateName):
    parks=[]   
    endpoint = requests.get(f"{url}/parks?stateCode={stateName}&api_key={api}")

    # Parse response
    data=endpoint.json()
    for park in data["data"]:
        parks.append(park["fullName"])
    return parks

#Generate a list of all the park names and the states to be used in the search bar
def listParksAndStates():            
    parks=[]
    states=set({})
    '''
    #only returns 50 parks by default. use to calculate total numb of parks 
    
    endpoint = requests.get(f"{url}/parks?api_key={api}")
    data = endpoint.json()      
    count=int(data["total"])
    
    #count ="500"
    #endpoint = requests.get(f"{url}/parks?limit={count}&api_key={api}")    
    #data = endpoint.json()

    #API seems to not function properly when making excessively large calls such as using limit="496", so multiple calls are made to the API to ensure it functions properly
    startCounter=1 
    limit=25
    while(startCounter<count):
        endpoint = requests.get(f"{url}/parks?limit={limit}&start={startCounter}&api_key={api}") 
        data = endpoint.json()
        for park in data["data"]:
            parks.append(park["fullName"])
            #if park extends over multiple states, append each state to a set
            if(len(park["states"])>2):
                for value in park["states"].split(","):
                    states.add(value)
        startCounter+=limit+1
    '''
    '''
    for park in data["data"]:
        parks.append(park["fullName"])
        #if park extends over multiple states, append each state to a set
        if(len(park["states"])>2):
            for value in park["states"].split(","):
                states.add(value)
    '''
    states = list(states)

    #sort alphabetically in place and return 
    parks.sort(), states.sort() 
    
    
    parks=["Alaskan National","Boulder Park", "Cayane Park", "Dora Park", "Yosemite", "Zion"]
    states=["AL","BC","CE","NJ","PT","YZ"]
    
    return parks, states

#infoType can equal "visitorCenters", "campgrounds", "alerts", "articles", "events", "news"
def getInfo(parkName, infoType):
    endpoint = requests.get(f"{url}/{infoType}?q={parkName}&api_key={api}")
    data = endpoint.json()  
    return data["data"]


def generateRandom(length, count):
    if length >= count:
        #Make sure random number is unique so same item from API doesn't show up
        random=[]
        while len(random)<count:
            x= randint(0,length-1)
            if x not in random:
                random.append(x)
    #Make sure random is in order so items are in chronological order from consuming API
    random.sort()
    return random


def parseRecurrence(rec):
    rrule=[]
    if rec=="":
        return  rrule   

    months={"01":"January", "02": "February", "03": "March", "04": "April","05":"May","06": "June", 
    "07":"July","08":"August","09":"September","10":"October","11":"November", "12":"December"}
    #Get the start and end date of the event. year of length 4, month of length 2, and day of length 2
    for i in range(0,2):
        baseIdx = rec.index("=")
        year=rec[baseIdx + 1 : baseIdx + 5]
        month=months[rec[baseIdx + 5 : baseIdx + 7]]
        day=rec[baseIdx + 7 : baseIdx + 9]
        rrule.append(month+" "+day+", "+year)
        rec=rec[baseIdx + 9::]
    
    days={"MO":"Monday", "TU":"Tuesday", "WE":"Wednesday", "TH":"Thursday", "FR":"Friday", "SA":"Saturday", "SU":"Sunday"}
    #If events recurs every single day, just append "day" ("every" will be the in html regardless)
    try:
        rec.index("FREQ=DAILY")
        
        rrule.append("day")
    except:
        #Gets the list of recurring days. "byday=" has length 6
        rec=rec[rec.index("BYDAY")+6::]
        rec=rec[0:rec.index(";")]    
        daysList=rec.split(",")
        for day in daysList:
            rrule.append(days[str(day)])    
    return rrule

def timeNeeded(startTime,endTime):
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





'''
checker=[]
eventsList=getInfo("Zion", "events")
for event in eventsList:
    eventTime= event.get("times")[0]
    print(event.get("title"))
    print(eventTime)
    checker.append(timeNeeded(eventTime.get("timestart"), eventTime.get("timeend")))
    print(timeNeeded(eventTime.get("timestart"), eventTime.get("timeend")))
    print()
    '''
'''
#print(getInfo("Zion","articles")[0])
#print(visitorCenters("Zion")[0]["name"])

#print(listParksByState("ME"))
#listParksAndStates()
#print(listParksAndStates()[0])
#print(listParksAndStates()[1])
'''
