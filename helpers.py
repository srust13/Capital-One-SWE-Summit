import requests, json

url="https://developer.nps.gov/api/v1/parks?"
api= "D2TLvUtbqv8zYCvVqc4baUmgc2UlET6nbdbtQsJX"

def numParksByState():
    # Contact API
    state="me"    
    endpoint = requests.get(f"{url}stateCode={state}&api_key={api}")

    # Parse response
    data=endpoint.json()
    numParks = data["total"]
    print("There are " + str(numParks) + " parks in " + state.upper() + ".")
    for park in data["data"]:
        print(park["name"])

#Generate a list of all the park names and the states to be used in the search bar
def listParksAndStates():        
    parks=[]
    states=set({})
    #only returns 50 parks by default. use to calculate total numb of parks 
    endpoint = requests.get(f"{url}api_key={api}")
    data = endpoint.json()   
    #count = data["total"]
    
    count=490
    endpoint = requests.get(f"{url}limit={count}&api_key={api}")
    data=endpoint.json()
    '''
    for park in data["data"]:
        parks.append(park["fullName"])
        #if park extends over multiple states, append each state to a set
        if(len(park["states"])>2):
            for value in park["states"].split(","):
                states.add(value)
    #states=list(states)
    for i in states:
        print(i)
    #sort alphabetically in place and return 
    #parks.sort(), states.sort() 
    return parks, states

'''
numParksByState()
#listParksAndStates()
#print(listParksAndStates()[0])
#print(listParksAndStates()[1])
