import pandas as pd
from geopy.distance import great_circle

# Load airports data
airports = pd.read_csv('using_folium/airports.dat', header=None)
airports.columns = ['id', 'name', 'city', 'country', 'iata', 'icao', 'lat', 'lon', 'alt', 'tz', 'dst', 'tz_db', 'type', 'source']
airports = airports[airports['iata'].notnull() & (airports['iata'] != '\\N')]

# Load routes data
routes = pd.read_csv('using_folium/routes.dat', header=None)
routes.columns = ['airline', 'airline_id', 'source', 'source_id', 'dest', 'dest_id', 'codeshare', 'stops', 'equipment']
routes = routes[routes['source'].isin(airports['iata']) & routes['dest'].isin(airports['iata'])]

# Merge coordinates
routes = routes.merge(airports[['iata', 'lat', 'lon']], left_on='source', right_on='iata')
routes = routes.rename(columns={'lat': 'source_lat', 'lon': 'source_lon'}).drop('iata', axis=1)
routes = routes.merge(airports[['iata', 'lat', 'lon']], left_on='dest', right_on='iata')
routes = routes.rename(columns={'lat': 'dest_lat', 'lon': 'dest_lon'}).drop('iata', axis=1)

# Estimate cost, time, and CO2
def estimate(row):
    distance_km = great_circle((row['source_lat'], row['source_lon']), (row['dest_lat'], row['dest_lon'])).km
    cost = round(distance_km * 0.08, 2)  # Assume $0.08 per km
    time = round(distance_km / 750 * 60, 2)  # Assume 750 km/h average speed
    co2 = round(distance_km * 0.115, 2)  # Assume 115g CO2 per km
    return pd.Series([cost, time, co2])

routes[['cost', 'time_minutes', 'co2_kg']] = routes.apply(estimate, axis=1)

# Save to CSV
routes[['source', 'dest', 'cost', 'time_minutes', 'co2_kg', 'source_lat', 'source_lon', 'dest_lat', 'dest_lon']].to_csv('flights.csv', index=False)
