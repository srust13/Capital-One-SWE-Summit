# Capital One Software Engineering Summit MindSumo Challenge

Website: https://

## Project Details

This web application serves as a sort of information kiosk for the [National Park Service](https://www.nps.gov/index.htm). Deatiled below is information on the technologies used and the features in the app, as well as why certain things were done the way they were. Also included are some accomplishments and challenged I faced along the way.

## List of APIs and tools used

- [National Park Service (NPS) API](https://www.nps.gov/subjects/developer/api-documentation.htm)
- [NPMap.js](https://www.nps.gov/subjects/developer/api-documentation.htm)
- [NPMap Symbols Library](https://github.com/nationalparkservice/symbol-library)
- [Google Maps API](https://developers.google.com/maps/documentation/)
   - Distance Matrix API to calculate distances between two points
   - Directions Service API to calculate an efficient route between two points
   - Maps JavaScript API to display a map and add any necessary features
- [Flask](http://flask.pocoo.org/docs/1.0/) for backend
- [Bootstrap](https://getbootstrap.com/docs/4.3) for frontend styling and [Jinja2](http://jinja.pocoo.org/docs/2.10/) for templating 
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse HTML pages from NPS

## The build

### Required features

#### Designation and state filtering
- Users can select either a park location to see that specific park, or select a state to see all the parks associated with that state. 

#### Name and keyword search
- Users can input a keyword to see all the parks associated with that keyword.

#### Displaying relevant park information, visitor centers, campgrounds, alerts, articles, events, news releases about a selected destination, as well as educational acitivites, relevant people, and places associated with the location
- Series of GET requests to the NPS API to display relevant information.
- Used Beautiful Soup to get the first image of the carousel since it makes for a nice banner picture (use NPS API for the rest of the images). Some of the pictures might not display perfectly because the dimensions of the carousel pictures are absolute to fit the page and the image from the NPS API has to conform to it. 

### Extra features

#### Displaying a route between the user and the selected destination
- Used HTML5 Geolocation to get the current location of the user and NPS API to get the location of the park.
- Used Google Maps JavaScript API to display an interactive map and Google Maps Direction Service API to calculate the route between the user and park.

#### Calculating distance of the associated route 
- Used Google Maps Distance Matrix API to calculate the distance from start to finish.

#### Using relevant symbols from the NPS symbols library
- Used NPS symbol library through CDN to display relevant information about the selected park.

#### Displaying NPMAP.js
- Display the NPMAP.js using NPMAP.js Bootstrap to display the locations of the parks within the continental US.

## Challenges
- Initially to compile a list of the parks (497 parks) and states (59 "states", better term is location since it includes non US locations like "Guam") that the user could choose from, I was using a request to the NPS API. However, the response took an extremely long time (~60 seconds) and would often crash, the reason for which is still unclear. Thus, Beautiful Soup was used to scrape data from the [National Park Service Advanced Search](https://www.nps.gov/findapark/advanced-search.htm) and this proved to be a more responsive and coherent solution.  
- Initially, when I was making requests to the NPS API, I would iterate over the JSON response and try to match the the selected park the user chose with the "fullName" key:value pair in the response. However, this didn't prove to be the best approach because some of the parks do not have proper names in the response (e.g. "Haleakal&amp;#257; National Park"). Also trying to pass along the park names between the HTML pages became cumbersome because of the encoding of special characters in the park names such as &, -, etc. To accomodate for this, any matching or passing of a park name that had to be done was done by using the 4 letter park code.  
- Some aspects of the NPS API seem to be broken. For example, the documentation mentions there will be at least one visitor center listed for each park and there will be at least one picture available for each campground. However, both cases are not true for all the parks listed.
- When making requests to the Google Maps Directions Service API using the latitude and longitude of the selected park, the response status was not always OK. This is most likely due to the location described by the latitude and longitude of the park not being accessible to by road. (e.g. Zion National Park). To work around this, instead of using the latitude and longitude position of the park, the park's name was used in the request to the Google Maps API. 

## Accomplishments
- Bringing forth a quality user experience in hopes of allowing people to understand more about national parks.
- Building a web application from ground up that has a lot of moving parts and getting the parts to work responsively and efficiently.
- Being exposed to JavaScript and its semantics, as well as learning about asynchronous calls and callbacks.