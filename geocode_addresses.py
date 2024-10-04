import csv
import requests
import time

API_KEY = 'AIzaSyCK2tZwA7IQM_uKCg527Sr2hyLd8eSo4QM'  # Replace with your Google Maps Geocoding API key

def geocode_address(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': API_KEY}
    response = requests.get(url, params=params)
    result = response.json()
    if result['status'] == 'OK':
        location = result['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Error geocoding {address}: {result['status']}")
        return None, None

input_file = 'restaurants.csv'
output_file = 'restaurants_geocoded.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Latitude', 'Longitude']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        address = row['Location']
        lat, lng = geocode_address(address)
        if lat and lng:
            row['Latitude'] = lat
            row['Longitude'] = lng
            print(f"Geocoded {row['Restaurant Name']}: {lat}, {lng}")
        else:
            row['Latitude'] = ''
            row['Longitude'] = ''
            print(f"Failed to geocode {row['Restaurant Name']}")
        writer.writerow(row)
        time.sleep(0.1)  # Sleep to respect API rate limits
