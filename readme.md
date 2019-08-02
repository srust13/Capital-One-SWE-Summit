# (Winner) Capital One Software Engineering Summit MindSumo Challenge

Website: https://shubhamrustagi-capitalone.herokuapp.com 

*Tip: If using a mobile device to access the link, request to see "Desktop site" on the browser as it will create for a better user experience. Some features might not appear properly on a mobile device.*

**Throughout the application, a particular search query may not work properly because it takes the API too long to respond for relatively large responses (timeout error) and the page will get redirected. If this happens, it's best to try 1-2 more times in hopes of getting a valid response within the allotted time. However, this could also happen if the search query does not have any results.** 

## Project Details

This web application serves as a virtual information kiosk for the [National Park Service](https://www.nps.gov/index.htm). Detailed below is information on the technologies used and the features in the app, as well as why certain things were done the way they were. Also included are some challenges I faced along the way and the accomplishments of the project.

## List of APIs and tools used

- [Flask](http://flask.pocoo.org/docs/1.0/) for backend
- [National Park Service (NPS) API](https://www.nps.gov/subjects/developer/api-documentation.htm)
- [Google Maps API](https://developers.google.com/maps/documentation/)
   - Distance Matrix API to calculate distances between two points
   - Directions Service API to calculate an efficient route between two points
   - Maps JavaScript API to display a map and add any necessary features
- [NPMap Symbol Library](https://github.com/nationalparkservice/symbol-library)
- [Bootstrap](https://getbootstrap.com/docs/4.3) for frontend styling and [Jinja2](http://jinja.pocoo.org/docs/2.10/) for templating 
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse HTML pages from National Park Service sites

*Note: The NPS API key is an environment variable defined in Heroku config vars. Therefore, if cloning this repo. and running it locally is desired, you must register for an API key [here](https://www.nps.gov/subjects/developer/get-started.htm). The Google Maps API couldn't be protected in the same manner considering that the key has to be included in the script tags of the HTMl in order to load the JS files and data from Google's servers. To remedy this situation, API key restrictions have been placed that allow it to be protected in a visible public domain.*

## The build

### Required features

#### Designation and state filtering
-  Users can select any designation or select a state to see all the parks associated with that state. The list of designations was compiled by calling the API with the list of all parks and hard coding the designation values. Hard coding the designation values was not desirable, but done because the API invariably fails when trying to access all the park names (see "Challenges" section). The designation search page sometimes takes an extended period of time to show results depending on the selected option, as it may have a relatively large JSON response size. The list of states was compiled with Beautiful Soup (for the same reason), parsing the NPS website.

#### Name and keyword search
- Users can select either a park name to see that specific park, or input a keyword to see all the parks associated with that keyword. The list of parks was compiled with Beautiful Soup, parsing the NPS website. For a keyword search, if the user clicks on a specific park from the generated list, the parkcode associated with that park is then passed as a string argument routed to the `search.html` page to display the park (if it exists).

#### Displaying relevant park information, visitor centers, campgrounds, alerts, articles, events, news releases about a selected destination, as well as educational acitivites, relevant people, and places associated with the location
- Series of GET requests to the NPS API to display relevant information.
- Used Beautiful Soup to get the first image of the carousel since it makes for a nice banner picture (use NPS API for the rest of the images). Some of the pictures might not display perfectly because the dimensions of the carousel pictures are absolute to fit the page and the image from the NPS API has to conform to it. 

### Extra features

#### Displaying a route between the user and the selected destination
- Used HTML5 Geolocation to get the current location of the user and NPS API to get the location of the selected park.
- Used Google Maps JavaScript API to display an interactive map and Google Maps Direction Service API to calculate the route between the user and park and display said route on the map. <br>
*Note: This feature will only work if the app is accessed using HTTPS (not HTTP) since SSL is required for HTML5 Geolocation to locate the user.*

#### Calculating distance of the associated route 
- Used Google Maps Distance Matrix API to calculate the distance from start point to finish point on the route shown in the map.

#### Using relevant symbols from the NPS symbols library
- Used NPS symbol library SVGs to display relevant information about the selected park.
- SVGs were chosen over PNGs for several reasons, some of being: 1) Faster loading times 2) Better resolution 3) More responsive
- All SVGs were placed in a separate file to create less cluttered and easily maintainable HTML docs.

## Challenges
- Initially to compile a list of the parks (497 parks) and states (59 "states", better term is location since it includes non US locations like "Guam") that the user could choose from, I was using a GET request to the NPS API for all the parks and states. However, the response took an extremely long time (~60 seconds) and would often crash unpredictably, returning with a 500 HTTP Internal Server Error. Thus, Beautiful Soup was used to scrape data from the [National Park Service Advanced Search](https://www.nps.gov/findapark/advanced-search.htm) and this proved to be a more responsive and coherent solution. To try and increase the response rate, I also tried asynchronous calls using Python's asyncio and running the request in the background, but these methods didn't produce any notable changes. Similarly, in terms of getting the designation values for all the parks, the API had to be requested multiple times, mostly returning with a HTTP 500 error or empty JSON response. When it finally returned with a non-empty JSON response, the response was taken and converted into HTML code and hard coded into `designation-search.html` so the API would not have to be requested each time. While not the optimal way, this was the only alternate method I could think of that did not require a request to be made each time. 

- When requesting certain states (i.e. "California"), designations (i.e. "park"), or keywords (i.e. "park") that are associated with a large number of parks, the API sometimes takes longer than 30 seconds to respond (or crashes) and this will cause Heroku to timeout the request and return an error message. To make this application scalable, it would probably be best to store the parks, states, and designation values into a database and query the database rather than request information from the API. Of course, this would add the extra problem of checking to see if values in the database are updated with current information from the NPS, but this shouldn't be too much of a problem.

- Some aspects of the NPS API seem to be broken. For example, the documentation mentions there will be at least one visitor center listed for each park and there will be at least one picture available for each campground. However, both cases are not true for all the parks listed. 

- When making requests to the Google Maps Directions Service API using the latitude and longitude of the selected park and the user, the response status was not always "OK". This is most likely due to the location described by the latitude and longitude of the park not being accessible to by road. (e.g. Zion National Park). However, putting in the same latitude and longitude of the park and of the user into Google Maps resulted in a feasible route. Therefore, Google Maps probably uses a different API than the Directions Service API. Nonetheless, to work around this, instead of using the latitude and longitude position of the park, the park's name was used in the request to the Google Maps API as a backup, in the event that the geocodes do not work properly. If the geocodes were not used, the user will be notified. 

## Accomplishments
- Bringing forth a quality user experience in hopes of helping to keep visitors informed, educated, and safe as they enjoy the parks with an intuitive and easy to navigate interface.
- Building a web application from ground up that has a lot of moving parts and uses a multitude of languages, packages, and APIs and integrating all the parts with one another to work responsively and efficiently.
- Being exposed to JavaScript and its semantics, as well as learning about asynchronous calls and callbacks.

*General Note: There are 2 layout files used in the Flask application to compensate for the fact that there are 2 different backgrounds and 2 different color schemes depending on the page you visit.*