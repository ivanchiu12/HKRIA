// script.js

document.addEventListener('DOMContentLoaded', () => {
    function initMap() {
      let map;
      let userMarker;
      let restaurantMarkers = [];
      let infoWindow;
  
      const toggleButton = document.getElementById('toggle-button');
      const sidebar = document.getElementById('sidebar');
  
      // Add event listener to the toggle button
      toggleButton.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
      });
  
      // Initialize the map centered on Hong Kong (will update to user's location)
      function initializeMap(position) {
        const userLatLng = position ? { lat: position.coords.latitude, lng: position.coords.longitude } : { lat: 22.3193, lng: 114.1694 };
  
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 16,
          center: userLatLng
        });
  
        // Add a marker for the user's location
        if (position) {
          userMarker = new google.maps.Marker({
            position: userLatLng,
            map: map,
            title: 'Your Location',
            icon: {
              url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            }
          });
        }
  
        infoWindow = new google.maps.InfoWindow();
  
        // Load restaurant data and process
        loadRestaurantData(userLatLng);
      }
  
      // Get user's location
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          position => {
            initializeMap(position);
          },
          error => {
            // Handle location access denial
            alert('Error: Unable to access your location. Displaying default location.');
            initializeMap(null);
          }
        );
      } else {
        alert('Geolocation is not supported by this browser.');
        initializeMap(null);
      }
  
      // Load restaurant data and process nearby restaurants
      function loadRestaurantData(userLatLng) {
        fetch('restaurants.json')
          .then(response => response.json())
          .then(data => {
            // Filter restaurants within 100 meters
            const nearbyRestaurants = data.filter(restaurant => {
              const lat = parseFloat(restaurant.Latitude);
              const lng = parseFloat(restaurant.Longitude);
              if (!isNaN(lat) && !isNaN(lng)) {
                const distance = getDistance(userLatLng.lat, userLatLng.lng, lat, lng);
                return distance <= 100; // distance in meters
              } else {
                console.warn(`Invalid coordinates for ${restaurant['Restaurant Name']}`);
                return false;
              }
            });
  
            // Display nearby restaurants
            displayRestaurants(nearbyRestaurants, userLatLng);
          })
          .catch(error => {
            console.error('Error fetching the restaurant data:', error);
            const restaurantList = document.getElementById('restaurant-list');
            restaurantList.innerHTML = '<p class="error-message">Failed to load restaurant data.</p>';
          });
      }
  
      // Display restaurants on map and sidebar
      function displayRestaurants(restaurants, userLatLng) {
        const bounds = new google.maps.LatLngBounds();
        bounds.extend(userLatLng); // Include user's location in bounds
  
        const restaurantList = document.getElementById('restaurant-list');
        restaurantList.innerHTML = ''; // Clear existing list
  
        restaurants.forEach(restaurant => {
          const lat = parseFloat(restaurant.Latitude);
          const lng = parseFloat(restaurant.Longitude);
          const position = { lat: lat, lng: lng };
  
          // Create a marker for each restaurant
          const marker = new google.maps.Marker({
            position: position,
            map: map,
            title: restaurant['Restaurant Name']
          });
  
          restaurantMarkers.push(marker);
          bounds.extend(position);
  
          // Info window content
          const infoContent = `
            <h3>${restaurant['Restaurant Name']}</h3>
            <p>${restaurant.Location}</p>
            <p>${restaurant.Timestamp}</p>
          `;
  
          // Click event for marker
          marker.addListener('click', function() {
            infoWindow.setContent(infoContent);
            infoWindow.open(map, marker);
          });
  
          // Add restaurant to sidebar
          const restaurantItem = document.createElement('div');
          restaurantItem.classList.add('restaurant-item');
  
          restaurantItem.innerHTML = `
            <div class="restaurant-name">${restaurant['Restaurant Name']}</div>
            <div class="restaurant-address">${restaurant.Location}</div>
          `;
  
          // Click event for sidebar item
          restaurantItem.addEventListener('click', () => {
            map.setCenter(position);
            map.setZoom(18);
            google.maps.event.trigger(marker, 'click');
            // Hide sidebar on mobile after selecting a restaurant
            if (window.innerWidth <= 768) {
              sidebar.classList.add('collapsed');
            }
          });
  
          restaurantList.appendChild(restaurantItem);
        });
  
        // Adjust map to show all markers
        map.fitBounds(bounds);
  
        // Handle case when no restaurants are nearby
        if (restaurants.length === 0) {
          restaurantList.innerHTML = '<p>No restaurants found within 100 meters of your location.</p>';
        }
      }
  
      // Function to calculate distance between two coordinates in meters
      function getDistance(lat1, lng1, lat2, lng2) {
        const R = 6371000; // Radius of the Earth in meters
        const dLat = toRad(lat2 - lat1);
        const dLng = toRad(lng2 - lng1);
        const a =
          Math.sin(dLat / 2) * Math.sin(dLat / 2) +
          Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
          Math.sin(dLng / 2) * Math.sin(dLng / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        const distance = R * c;
        return distance;
      }
  
      // Converts numeric degrees to radians
      function toRad(value) {
        return value * Math.PI / 180;
      }
    }
  
    // Initialize the map when the DOM is fully loaded
    initMap();
  });
  