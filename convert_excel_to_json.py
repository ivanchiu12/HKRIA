import pandas as pd
import requests
import time
import json

# Replace with your actual Google Maps Geocoding API key
API_KEY = 'AIzaSyCK2tZwA7IQM_uKCg527Sr2hyLd8eSo4QM'

def geocode_address(address):
    """
    Geocode an address using the Google Maps Geocoding API.
    """
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching data for {address}: HTTP {response.status_code}")
        return None, None
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Geocoding error for {address}: {data['status']}")
        return None, None

def main():
    # Read the Excel file
    df = pd.read_excel('geomap_restaurant.xlsx')

    # Ensure the DataFrame has the necessary columns
    required_columns = ['Restaurant Name', 'Location', 'Timestamp']
    if not all(column in df.columns for column in required_columns):
        print("Error: Excel file must contain 'Restaurant Name', 'Location', and 'Timestamp' columns.")
        return

    # Add columns for Latitude and Longitude
    df['Latitude'] = None
    df['Longitude'] = None

    # Geocode each address
    for index, row in df.iterrows():
        address =row['Restaurant Name'] +','+ row['Location']
        print(f"Geocoding address: {address}")
        lat, lng = geocode_address(address)
        if lat and lng:
            df.at[index, 'Latitude'] = lat
            df.at[index, 'Longitude'] = lng
            print(f"Coordinates: {lat}, {lng}")
        else:
            print(f"Failed to geocode address: {address}")
        # Sleep to respect API rate limits
        time.sleep(0.2)  # Adjust delay as needed

    # Convert DataFrame to JSON
    df.to_json('restaurants.json', orient='records', force_ascii=False, indent=2)

    print('Excel file converted to JSON with latitude and longitude successfully.')

if __name__ == '__main__':
    main()
