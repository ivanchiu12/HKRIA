from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from geopy.distance import geodesic

app = Flask(__name__)

# Replace with your Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyCK2tZwA7IQM_uKCg527Sr2hyLd8eSo4QM'

# Load restaurant data from Excel
EXCEL_FILE_PATH = 'restaurants.xlsx'
if os.path.exists(EXCEL_FILE_PATH):
    df_restaurants = pd.read_excel(EXCEL_FILE_PATH)
    df_restaurants = df_restaurants.dropna(subset=['Latitude', 'Longitude'])
    df_restaurants['Latitude'] = pd.to_numeric(df_restaurants['Latitude'], errors='coerce')
    df_restaurants['Longitude'] = pd.to_numeric(df_restaurants['Longitude'], errors='coerce')
    df_restaurants = df_restaurants.dropna(subset=['Latitude', 'Longitude'])
else:
    df_restaurants = pd.DataFrame(columns=['Restaurant Name', 'Latitude', 'Longitude', 'District', 'Cuisines', 'Price_Range', 'Timestamp'])

@app.route('/')
def index():
    return render_template('index.html', api_key=GOOGLE_MAPS_API_KEY)

@app.route('/nearby_restaurants', methods=['GET'])
def nearby_restaurants():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    user_location = (latitude, longitude)
    nearby_restaurants = []

    for _, row in df_restaurants.iterrows():
        restaurant_location = (row['Latitude'], row['Longitude'])
        distance = geodesic(user_location, restaurant_location).meters
        if distance <= 1000:
            nearby_restaurants.append(row.to_dict())

    # Debug log for nearby restaurants
    print(f"User Location: {user_location}")
    print(f"Nearby Restaurants (within 100 meters): {nearby_restaurants}")

    return jsonify(nearby_restaurants)

if __name__ == '__main__':
    app.run(debug=True)