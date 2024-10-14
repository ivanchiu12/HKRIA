from flask import Flask, render_template, request, jsonify
import json
import os
from geopy.distance import geodesic

app = Flask(__name__)

# Replace with your Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyCK2tZwA7IQM_uKCg527Sr2hyLd8eSo4QM'

# Load restaurant data from JSON
JSON_FILE_PATH = 'restaurants.json'
if os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, 'r') as file:
        df_restaurants = json.load(file)
else:
    df_restaurants = []

@app.route('/')
def index():
    return render_template('index.html', api_key=GOOGLE_MAPS_API_KEY)

@app.route('/nearby_restaurants', methods=['GET'])
def nearby_restaurants():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    user_location = (latitude, longitude)
    nearby_restaurants = []

    for restaurant in df_restaurants:
        restaurant_location = (restaurant['Latitude'], restaurant['Longitude'])
        distance = geodesic(user_location, restaurant_location).meters
        if distance <= 1000:
            nearby_restaurants.append(restaurant)

    # Debug log for nearby restaurants
    print(f"User Location: {user_location}")
    print(f"Nearby Restaurants (within 100 meters): {nearby_restaurants}")

    return jsonify(nearby_restaurants)

if __name__ == '__main__':
    app.run(debug=True)