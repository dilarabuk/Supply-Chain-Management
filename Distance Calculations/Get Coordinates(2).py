
#Ülkelerin Koordinatlarını Çekiyoruz.
import pandas as pd
from geopy.geocoders import Nominatim

# Excel dosyasını oku
excel_file_path = 'largest_cities.xlsx'  # Excel dosyasının yolu
df = pd.read_excel(excel_file_path)

geolocator = Nominatim(user_agent="my_geocoder")

countries_coordinates = {"Countries": [], "Coordinates": []}

def get_country_coordinates(country_name):
    location = geolocator.geocode(country_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None

for country_name in df["C1"]:
    if country_name not in countries_coordinates["Countries"]:
        coordinates = get_country_coordinates(country_name)
        if coordinates:
            countries_coordinates["Countries"].append(country_name)
            countries_coordinates["Coordinates"].append(coordinates)

df_coordinates = pd.DataFrame(countries_coordinates)
df_coordinates.to_excel('CitiesCoordinates.xlsx', index=False)
print('Saved Succesfully to CitiesCoordinates.xlsx')
