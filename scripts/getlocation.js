
var x = document.getElementById("long");
var y = document.getElementById("lat");
var position;
function getLocation() {
    if (navigator.geolocation) {
        position = navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    console.log(position);
    y.innerHTML = "Latitude: " + position.coords.latitude;
    x.innerHTML = "Longitude: " + position.coords.longitude;
}

$(document).ready(getLocation);
