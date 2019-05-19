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

def listParks():
        
        parks=[]
        endpoint= requests.get(f"{url}api_key={api}")
        data=endpoint.json()
        parks.append(data["data"]["fullName"])

        for park in parks:
                print


#numParksByState()
listParks()

