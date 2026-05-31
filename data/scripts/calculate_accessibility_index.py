import pandas as pd
import numpy as np

print("=== Calculating Accessibility Index ===\n")

# 1. Load Restaurants
rest = pd.read_csv('data/restaurants_clean.csv')
print(f"Loaded {len(rest)} food venues")

# 2. Load Transport Stops (simple version - convert from geojson)
import json
with open('data/public_transport_stops.geojson', 'r', encoding='utf-8') as f:
    geo_data = json.load(f)

stops_list = []
for feature in geo_data['features']:
    stops_list.append({
        'STOP_NAME': feature['properties'].get('STOP_NAME'),
        'MODE': feature['properties'].get('MODE'),
        'Longitude': feature['geometry']['coordinates'][0],
        'Latitude': feature['geometry']['coordinates'][1]
    })

stops = pd.DataFrame(stops_list)
print(f"Loaded {len(stops)} transport stops")

# Filter Train + Tram only
stops = stops[stops['MODE'].isin(['METRO TRAIN', 'Tram', 'Train'])]

print(f"Using {len(stops)} Train + Tram stops for index")

# 3. Calculate distance from CBD
cbd_lat, cbd_lon = -37.813, 144.963

def haversine_dist(lat1, lon1, lat2=cbd_lat, lon2=cbd_lon):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

rest['dist_to_cbd'] = haversine_dist(rest['Latitude'], rest['Longitude'])
stops['dist_to_cbd'] = haversine_dist(stops['Latitude'], stops['Longitude'])

# Create distance bands
bands = [0, 2, 5, 10, 20]
labels = ['CBD (0-2km)', 'Inner (2-5km)', 'Middle (5-10km)', 'Outer (10-20km)']

rest['band'] = pd.cut(rest['dist_to_cbd'], bins=bands, labels=labels)
stops['band'] = pd.cut(stops['dist_to_cbd'], bins=bands, labels=labels)

# Summary
summary = pd.DataFrame({
    'Area': labels,
    'Food_Venues': rest.groupby('band').size().values,
    'Train_Tram_Stops': stops.groupby('band').size().values
})

summary['Food_per_Stop'] = round(summary['Food_Venues'] / summary['Train_Tram_Stops'], 2)
summary['Accessibility_Score'] = summary['Food_Venues'] * 0.6 + summary['Train_Tram_Stops'] * 0.4

print("\n✅ ACCESSIBILITY INDEX:")
print(summary.round(2))

summary.to_csv('data/accessibility_index.csv', index=False)
print("\n✅ Saved to data/accessibility_index.csv")