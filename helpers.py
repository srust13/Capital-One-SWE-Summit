import requests, json
import urllib.request, json

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

        

print(getInfo("Zion","articles")[0])
#print(visitorCenters("Zion")[0]["name"])

#print(listParksByState("ME"))
#listParksAndStates()
#print(listParksAndStates()[0])
#print(listParksAndStates()[1])
