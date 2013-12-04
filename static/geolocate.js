/**
* geolocate.js
*/
if(!jQuery) {
  throw new Error("Requires jQuery");
}
function setLocation(position) {
  $( ".latitude" ).filter( ":input").val(position.coords.latitude)
  $( ".longitude" ).filter( ":input").val(position.coords.longitude)
  $( ".latitude" ).filter( ":not(:input)").text(position.coords.latitude)
  $( ".longitude" ).filter( ":not(:input)").text(position.coords.longitude)
}
if (navigator.geolocation) {
  if( $( ".latitude" ).length || $( ".longitude" ).length ) {
    navigator.geolocation.watchPosition(setLocation);
  }
}