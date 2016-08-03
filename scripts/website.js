// var map;
// var service;
// var infowindow;

// function initialize() {
//   var newyork = new google.maps.LatLng(40,-74);
//
//   map = new google.maps.Map(document.getElementById('map-canvas'), {
//       center: newyork,
//       zoom: 8
//     });
//
//   var request = {
//     location: newyork,
//     radius: '500',
//     query: 'restaurant'
//   };
//
//
//   google.maps.event.addDomListener(window, 'load', initialize);
//   service = new google.maps.places.PlacesService(map);
//   service.textSearch(request, callback);
// }

// Initialization for the Maps APIs
function partyFunction() {
   var mapOptions = {
     center: new google.maps.LatLng(40,-74),
     zoom: 8
   };
   map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
}

google.maps.event.addDomListener(window, "load", partyFunction);
// The google Map frame has a number of events like any other HTML element.
// Here we set an handler to inialize the map when the map loads. You can
// add listeners for "click", "move" and so on...
// google.maps.event.addDomListener(window, 'load', initialize);











//Technical map options here
// function callback(results, status) {
//   if (status == google.maps.places.PlacesServiceStatus.OK) {
//     for (var i = 0; i < results.length; i++) {
//       var place = results[i];
//       createMarker(results[i]);
//     }
//   }
// }
