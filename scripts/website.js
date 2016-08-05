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

var cent_lat = $("#center_data").attr("cent_lat");
var cent_long = $("#center_data").attr("cent_long");
var place_type = $("#center_data").attr("place_type"); // var variable that references that user input
console.log(place_type);

function partyFunction() {
    console.log("Party!!!! " + cent_lat + " " + cent_long);
    var coord = new google.maps.LatLng(cent_lat,cent_long);
    map = new google.maps.Map(document.getElementById('map-canvas'), {
      center: coord,
      zoom: 15
    });

/// instantiate a variable named request pass in three arguments such as location,
// radius and the query
  var request = {
    location: coord,
    radius: '500',
    query: ['{{place_type|' + place_type + '}}']
  };

//copy the procedure for building a map and place it in a variable called service
  service = new google.maps.places.PlacesService(map);
  service.textSearch(request, callback)
}

markers = [];

function print_place(place) {
  $('#map-info').append(
    "<h1 class='header'>Place Info  </h1> <br>" +
    "Place name:  <b>" +
    place.name + "</b>" +
    "<br> Place address:  <b>        </b>" +
    place.formatted_address + "</b>"
  );
  console.log(place);
}

function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      var place = results[i];
      var marker = new google.maps.Marker({
          map: map,
          position: place.geometry.location,
          info: place,
        });
      markers.push(marker);
      console.log(place);
      google.maps.event.addListener(markers[i],
              'click',
              function() {
                print_place(this.info);
              }
      );
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
