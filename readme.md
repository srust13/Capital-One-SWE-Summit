# Capital One Software Engineering Summit MindSumo Challenge

Website: https://shubhamrustagi-capitalone.herokuapp.com/search

## Project Details

This web application serves as a sort of information kiosk for the [National Park Service](https://www.nps.gov/index.htm). Deatiled below is information on the technologies used and the features in the app, as well as why certain things were done the way they were. Also included are some accomplishments and challenged I faced along the way.

## List of APIs and tools used

- [National Park Service (NPS) API](https://www.nps.gov/subjects/developer/api-documentation.htm)
- [NPMap Symbols Library](https://github.com/nationalparkservice/symbol-library)
- [Google Maps API](https://developers.google.com/maps/documentation/)
   - Distance Matrix API to calculate distances between two points
   - Directions Service API to calculate an efficient route between two points
   - Maps JavaScript API to display a map and add any necessary features
- [Flask](http://flask.pocoo.org/docs/1.0/) for backend
- [Bootstrap](https://getbootstrap.com/docs/4.3) for frontend styling and [Jinja2](http://jinja.pocoo.org/docs/2.10/) for templating 
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse HTML pages from NPS

*Note: The NPS API key is an environment variable defined in Heroku config vars. Therefore, if cloning this repo. is desired and running it, you must register for an API key [here](https://www.nps.gov/subjects/developer/get-started.htm). The Google Maps API couldn't be protected in the same manner considering that the key has to be included in the script tags of the HTMl in order to load the JS files and data from Google's servers. To remedy this situation, API key restrictions have been placed that allow it to be protected in a visible public domain.*

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
- Used Google Maps JavaScript API to display an interactive map and Google Maps Direction Service API to calculate the route between the user and park and display said route on the map.

#### Calculating distance of the associated route 
- Used Google Maps Distance Matrix API to calculate the distance from start to finish.

#### Using relevant symbols from the NPS symbols library
- Used NPS symbol library SVGs to display relevant information about the selected park.
- SVGs were chosen over PNGs for several reasons, some of being: 1) Faster loading times 2) Better resolution 3) More responsive
- All SVGs were placed in a seperate file to create a less cluttered and easily mutable HTML document.

## Challenges
- Initially to compile a list of the parks (497 parks) and states (59 "states", better term is location since it includes non US locations like "Guam") that the user could choose from, I was using a request to the NPS API. However, the response took an extremely long time (~60 seconds) and would often crash, the reason for which is still unclear. Thus, Beautiful Soup was used to scrape data from the [National Park Service Advanced Search](https://www.nps.gov/findapark/advanced-search.htm) and this proved to be a more responsive and coherent solution.  
- Initially, when I was making requests to the NPS API, I would iterate over the JSON response and try to match the the selected park the user chose with the "fullName" key:value pair in the response. However, this didn't prove to be the most optimal approach as many names had HTML characters in their name (e.g. "Haleakal&amp;#257; National Park"; "&amp;#257;" is the HTML code to display an accented a). Also trying to pass along the park names between the HTML pages became cumbersome because of the HTML encoding of special characters in the park names such as &, -, etc. Dealing with this wouldn't be too difficult with Python, but would add unnecessariy complexity and verbosity to the code. To accomodate for this, any matching or passing of a park name that had to be done was done by using a much simpler 4 letter park code.  
- Some aspects of the NPS API seem to be broken. For example, the documentation mentions there will be at least one visitor center listed for each park and there will be at least one picture available for each campground. However, both cases are not true for all the parks listed.
- When making requests to the Google Maps Directions Service API using the latitude and longitude of the selected park, the response status was not always OK. This is most likely due to the location described by the latitude and longitude of the park not being accessible to by road. (e.g. Zion National Park). However, putting in the same latitude and longitude of the park and of the user into Google Maps resulted in a feasible route. So it's plausible Google Maps uses a different API than the Directions Service API. Nonetheless, to work around this, instead of using the latitude and longitude position of the park, the park's name was used in the request to the Google Maps API. 

## Accomplishments
- Bringing forth a quality user experience in hopes of allowing people to understand more about national parks.
- Building a web application from ground up that has a lot of moving parts and uses a multitude of languages, packages, and APIS and integrating all the parts with one another to work responsively and efficiently.
- Being exposed to JavaScript and its semantics, as well as learning about asynchronous calls and callbacks.