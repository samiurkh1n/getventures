var map;
var service;
var infowindow;

function initialize() {
  var newyork = new google.maps.LatLng(40,-74);

  map = new google.maps.Map(document.getElementById('map'), {
      center: newyork,
      zoom: 15
    });

  var request = {
    location: newyork,
    radius: '500',
    query: 'restaurant'
  };

  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, callback);
}

function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      var place = results[i];
      createMarker(results[i]);
    }
  }
}