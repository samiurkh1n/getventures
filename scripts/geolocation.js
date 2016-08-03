
// This if statement will ask the browser to prompt the user to allow location to be requested.
if (navigator.geolocation) {
navigator.geolocation.getCurrentPosition(function(position) {

// Gets the lat and the lng and stores it in to variable pos
var pos = {
  lat: position.coords.latitude,
  lng: position.coords.longitude
};
  function() {
  handleLocationError(true, infoWindow, map.getCenter());
  } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }


      function handleLocationError(browserHasGeolocation, pos) {
                      print  'Error: The Geolocation service failed.' :
                      print  'Error: Your browser doesn\'t support geolocation.');
      }




    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCZ6OqnPOFlTvJtrAbtdjkFocL0i_68AZI&callback=initMap">
