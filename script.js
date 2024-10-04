// script.js

function initMap() {
    // Center the map on Hong Kong
    var mapCenter = { lat: 22.3193, lng: 114.1694 };
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
      center: mapCenter
    });
  
    // Fetch the restaurant data
    fetch('restaurants.json')
      .then(response => response.json())
      .then(data => {
        data.forEach(restaurant => {
          // Ensure latitude and longitude are numbers
          var lat = parseFloat(restaurant.Latitude);
          var lng = parseFloat(restaurant.Longitude);
  
          if (!isNaN(lat) && !isNaN(lng)) {
            var position = { lat: lat, lng: lng };
  
            var marker = new google.maps.Marker({
              position: position,
              map: map,
              title: restaurant['Restaurant Name']
            });
  
            var infoWindow = new google.maps.InfoWindow({
              content: `
                <h3>${restaurant['Restaurant Name']}</h3>
                <p>${restaurant.Location}</p>
                <p>${restaurant.Timestamp}</p>
              `
            });
  
            marker.addListener('click', function() {
              infoWindow.open(map, marker);
            });
          } else {
            console.warn(`Invalid coordinates for ${restaurant['Restaurant Name']}`);
          }
        });
      })
      .catch(error => {
        console.error('Error fetching the restaurant data:', error);
      });
  }
  
  // Initialize the map when the window loads
  window.onload = initMap;
  