
$(document).ready(function() {
  jQuery.fn.carousel.Constructor.TRANSITION_DURATION = 4000  // 4 seconds (carousel interval to switch pictures)
  });
  
      
  function mapLocation(park, lat, long) {        
      var directionsDisplay; 
      var map;
      var alternate;
      var start;
      var end;        
      let directionsService = new google.maps.DirectionsService();        
      let x = document.getElementById("info");
      
      // Render map and listen for if user clicks route button
      function initialize() {
          directionsDisplay = new google.maps.DirectionsRenderer();
          
          // Geocode for Lebanon, Kansas (approximately geographic center of USA)
          let mapCenter = new google.maps.LatLng(39.809860, -98.555183);
          let mapOptions = {zoom: 4, center: mapCenter};
          map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
          directionsDisplay.setMap(map);
          google.maps.event.addDomListener(document.getElementById('routebtn'), 'click', getLocation);
      }
  
      // Get the current location of the user and display the route from the user to the respective park on the map. 
      function getLocation() 
      {
          if (navigator.geolocation) 
          {
              navigator.geolocation.getCurrentPosition(calcRoute, showError);
          } 
          else 
          { 
              x.innerHTML = "Geolocation is not supported by this browser.";
          }
      }
  
      // Error cases
      function showError(error) 
      {
          switch(error.code) 
          {
              case error.PERMISSION_DENIED:
                  x.innerHTML = "User denied the request for Geolocation.";
              break;
              case error.POSITION_UNAVAILABLE:
                  x.innerHTML = "Location information is unavailable.";
              break;
              case error.TIMEOUT:
                  x.innerHTML = "The request to get user location timed out.";
              break;
              case error.UNKNOWN_ERROR:
                  x.innerHTML = "An unknown error occurred.";
              break;
          }
      }
      
      // Display route on the map
      function calcRoute(position) 
      {
          // Keeps track of if the alternateParkString is used (if geocodes of park don't suffice, we will use the name of the park for the Google Maps API request )
          alternate=false;
  
          // User location
          start = new google.maps.LatLng(position.coords.latitude , position.coords.longitude);
          // Park location
          end = new google.maps.LatLng(lat,long);
          
          alternateParkString=park;
          
          // Markers for map. Start is user and end is park
          let startMarker = new google.maps.Marker({position: start, animation: google.maps.Animation.DROP, map: map});
          let endMarker = new google.maps.Marker({position: end, animation: google.maps.Animation.DROP, map: map});
          
          let bounds = new google.maps.LatLngBounds();
          bounds.extend(start);
          bounds.extend(end);
          map.fitBounds(bounds);
          
          // API request given latitude and longitude information of both user and park
          let request = {origin: start, destination: end, travelMode: google.maps.TravelMode.DRIVING};
          directionsService.route(request, function (response, status) 
          {
              if (status == google.maps.DirectionsStatus.OK) 
              {
                  directionsDisplay.setDirections(response);
                  directionsDisplay.setMap(map);
                  getDistance();
                  x.innerHTML=("");
              } 
              else 
              {
                  //Use the name of the park since the latitude longitude provided by NPS isn't acessible by road (view README)
                  let request = {origin: start, destination: alternateParkString, travelMode: google.maps.TravelMode.DRIVING};
                  directionsService.route(request, function (response, status) 
                  {
                      if (status == google.maps.DirectionsStatus.OK) 
                      { 
                          alternate=true;
                          x.innerHTML= ("We could not find the exact route since the geographic coordinates provided by the National Park Service aren't acessible by road. Your destination has been redirected to as close as we could get for " +park+". <br/><br/>");                      
                          directionsDisplay.setDirections(response);
                          directionsDisplay.setMap(map);
                      } 
                      else
                      {
                          alternate=true;
                          x.innerHTML=("Directions request from "+park+" to your location could not be found.");
                      }
                      getDistance();
                  });
              }
          });  
      }
  
  
      //Get the distance and duration it would take to get from user location to park location
      function getDistance()
      {                 
          let service = new google.maps.DistanceMatrixService();
          
          // destination is the parks latitude and longitude information, unless the geoCodes didn't work, in which case destination will be the string literal park name
          let destination=end;
      
          if (alternate==true)
          {
              destination=alternateParkString;   
          }
  
          // API request for distance between 2 points
          service.getDistanceMatrix({
              origins: [start],
              destinations: [destination],
              travelMode: google.maps.TravelMode.DRIVING,
              unitSystem: google.maps.UnitSystem.METRIC,
              avoidHighways: false,
              avoidTolls: false,
          }, 
          function(response, status) {
              
              if (status !== 'OK') 
              {
                  alert('Error was: ' + status);
              } 
              else 
              {            
                  let km_distance=response.rows[0].elements[0].distance.text;
                  
                  // Exclude the units in the response and any commas
                  km_distance=km_distance.slice(0,km_distance.indexOf("km")).replace(",", "");
                  
                  // Convert km to miles
                  let miles_distance= km_distance*0.621371;                    
                  x.innerHTML+="The distance from your current location to "+park+ " is: " +miles_distance.toFixed(3)+" miles. If you drove non-stop, the drive would take you: "+response.rows[0].elements[0].duration.text+".";
              }                
          });
      }
      google.maps.event.addDomListener(window, 'load', initialize);
  }
  
  
      
  