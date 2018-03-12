// placing all event pins by loading the geolocation data from DB
// Request lat & lng data from the endpoint
function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 37.781715, lng:-122.408367} //Holberton Address. REVISIT
  });

  $.ajax({
    url: 'http://0.0.0.0:5000/api/all_events',
    dataType: 'json',
    type: 'GET',
    success: function(data){
      var infowindow = new google.maps.InfoWindow();

      var marker, i;
      for (i = 0; i < Object.keys(data).length; i++) {
        marker = new google.maps.Marker({
          position: new google.maps.LatLng(data[i].location.lat, data[i].location.lon),
          map: map
        });

	google.maps.event.addListener(marker, 'click', (function(markerObj, event_key) {
          return function() {
            infowindow.setContent('<h3><b>' + data[event_key].name + '</b></h3>'
				 + '<p>Address: ' + data[event_key].address + '</p>'
				 + '<p>Date: ' + data[event_key].date + '</p>'
				 + '<p>Time: ' + data[event_key].time + '</p>'
				 + '<p>Tags: ' + data[event_key].tags + '</p>');
            infowindow.open(map, markerObj);
          }
        })(marker, i));
      }
    },
    error: function(){
      console.log("error");
    }
  });
}
