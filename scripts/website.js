 var map;
 var service;
 var infowindow;

// Initialization for the Maps APIs
// function partyFunction() {
//    var mapOptions = {
//      center: new google.maps.LatLng(40.7503973,-74.3159636),
//      zoom: 8
//    };
//    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
//
//   }
// google.maps.event.addDomListener(window, "load", partyFunction);



//This function is going to display the map on the website using a already
// pre-installed latitude and longitude coordinates

function partyFunction() {
  var newyork = new google.maps.LatLng(40.7503973,-74.3159636);
   map = new google.maps.Map(document.getElementById('map-canvas'), {
      center: newyork,
      zoom: 15
    });

/// instantiate a variable named request pass in three arguments such as location,
// radius and the query
  var request = {
    location: newyork,
    radius: '500',
    query: ['store']
  };

//copy the procedure for building a map and place it in a variable called service 
  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, callback)
}
function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      var place = results[i];
      var marker = new google.maps.Marker({
          map: map,
          position: place.geometry.location
        });
      //createMarker(results[i]);
    }
  }
}
google.maps.event.addDomListener(window, "load", partyFunction);
// function callback(results, status) {
//   if (status == google.maps.places.PlacesServiceStatus.OK) {
//     for (var i = 0; i < results.length; i++) {
//       var place = results[i];
//       createMarker(results[i]);
//     }
//   }
// }
