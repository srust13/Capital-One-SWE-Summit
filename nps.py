import requests, json

def contact():
    
    # Contact API
    state="me"
    api= "D2TLvUtbqv8zYCvVqc4baUmgc2UlET6nbdbtQsJX"
    endpoint = requests.get(f"https://developer.nps.gov/api/v1/parks?stateCode={state}&api_key={api}")

    # Parse response
    data=endpoint.json()
    numParks = data["total"]
    print("There are " + str(numParks) + " parks in " + state.upper() + ".")
    for park in data["data"]:
        print(park["name"])
   
contact()