# Capital One Software Engineering Summit MindSumo Challenge

Website: https://shubhamrustagi-capitalone.herokuapp.com 

*Tip: If using a mobile device to access the link, request to see "Desktop site" on the browser as it will create for a better user experience. Some features might not appear properly on a mobile device.*

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
-  Users can select any designation or select a state to see all the parks associated with that state. The list of designations was run by calling the API with the list of all parks and hard coding the designation values. Hard coding the designation values was not desirable, but done because the API invariably fails when trying to access all the park names (see "Challenges" section). The designation search page sometimes takes an extend period of time to show results depending on the selected option, as it has a relatively large JSON response size. The list of parks and states was compiled with Beautiful Soup, parsing the NPS website.

#### Name and keyword search
- Users can select either a park name to see that specific park, or input a keyword to see all the parks associated with that keyword. For a keyword search, if the user clicks on a specific park from the generated list, the parkcode associated with that park is then passed as a string argument routed to the `search.html` page to display the park (if it exists).

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
- Initially to compile a list of the parks (497 parks) and states (59 "states", better term is location since it includes non US locations like "Guam") that the user could choose from, I was using a GET request to the NPS API. However, the response took an extremely long time (~60 seconds) and would often crash unpredictably. Thus, Beautiful Soup was used to scrape data from the [National Park Service Advanced Search](https://www.nps.gov/findapark/advanced-search.htm) and this proved to be a more responsive and coherent solution. In terms of getting the designation values for all the parks, the API had to be requested multiple times and when it finally returned with a non-empty JSON response, the response was taken and converted into HTML code and hard coded into `designation-search.html`. While not the optimal way, this was the only alternate method I could think of that did not require a request to be made. <br>**Throughout the application, the API GET request may not work properly because it takes too long to respond for relatively large responses (timeout error) and the page will get redirected. If this happens, it's best to try 1-2 more times in hopes of getting a valid response within the alotted time. However, this could also happen if the search result does not have any results.** 

- Initially, when I was making requests to the NPS API, I would iterate over the JSON response and try to match the selected park the user chose with the "fullName" key:value pair in the response. However, this didn't prove to be the most optimal approach as many names had HTML characters in their name (e.g. "Haleakal&amp;#257; National Park"; "&amp;#257;" is the HTML code to display an accented a). Also trying to pass along the park names between the HTML pages became cumbersome because of the HTML encoding of special characters in the park names such as &, -, etc. Dealing with this would not be difficult with Python, but would add unnecessary complexity and verbosity to the code. To accommodate for this, any matching or passing of a park name that had to be done was done by using a much simpler 4 letter park code.  

- Some aspects of the NPS API seem to be broken. For example, the documentation mentions there will be at least one visitor center listed for each park and there will be at least one picture available for each campground. However, both cases are not true for all the parks listed.

- When making requests to the Google Maps Directions Service API using the latitude and longitude of the selected park and the user, the response status was not always OK. This is most likely due to the location described by the latitude and longitude of the park not being accessible to by road. (e.g. Zion National Park). However, putting in the same latitude and longitude of the park and of the user into Google Maps resulted in a feasible route. So it's plausible Google Maps uses a different API than the Directions Service API. Nonetheless, to work around this, instead of using the latitude and longitude position of the park, the park's name was used in the request to the Google Maps API as a backup, should the geocodes not work properly. If the geocodes were not used, the user will be notified. 

## Accomplishments
- Bringing forth a quality user experience in hopes of allowing people to the best National Park experience possible with an intuitive, easy to navigate interface.
- Building a web application from ground up that has a lot of moving parts and uses a multitude of languages, packages, and APIs and integrating all the parts with one another to work responsively and efficiently.
- Being exposed to JavaScript and its semantics, as well as learning about asynchronous calls and callbacks.

*General Note: There are 2 layout files used in the Flask application to compensate for the fact that there are 2 different backgrounds and 2 different color schemes depending on the page you visit.*