/**
 * Created by rishi on 4/13/16.
 */

jQuery(function($) {
    // Asynchronously Load the map API
    var script = document.createElement('script');
    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAVhwXSYEzZbFblTqNsYg2lH-nhduepgPc&callback=initialize";
    document.body.appendChild(script);
});

function initialize() {

    var sensorLatLong = document.getElementById("map-script").getAttribute("location-data");
    console.log(sensorLatLong);


    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };

    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    map.setTilt(45);

    // Multiple Markers
    //var markers = [
    //    ['Morro_Bay_-_T_Pier', 35.365, -120.857],
    //    ['Monterey', 36.605, -121.889],
    //    ['Humboldt', 40.777, -124.196],
    //    ['Bodega_Bay', 38.316, -123.070]
    //];

    var markers = JSON.parse(sensorLatLong);
    // Info Window Content
    //var infoWindowContent = [
    //    ['<div class="info_content">' +
    //    '<h3>Sea water temperature</h3>' +
    //    '<p></p>' +        '</div>'],
    //    ['<div class="info_content">' +
    //    '<h3>Sea water pressure</h3>' +
    //    '<p></p>' +
    //    '</div>'],
    //    ['<div class="info_content">' +
    //    '<h3>Turbidity</h3>' +
    //    '<p></p>' +
    //    '</div>'],
    //    ['<div class="info_content">' +
    //    '<h3>Sea water pressure</h3>' +
    //    '<p></p>' +
    //    '</div>']
    //];

    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow(), marker, i;

    // Loop through our array of markers & place each one on the map
    for( i = 0; i < markers.length; i++ ) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: markers[i][0]
        });

        // Allow each marker to have an info window
        //google.maps.event.addListener(marker, 'click', (function(marker, i) {
        //    return function() {
        //        infoWindow.setContent(infoWindowContent[i][0]);
        //        infoWindow.open(map, marker);
        //    }
        //})(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }

    // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        this.setZoom(6);
        google.maps.event.removeListener(boundsListener);
    });

}
