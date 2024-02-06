import requests
from bs4 import BeautifulSoup
import pandas as pd
import copy
from geopy.distance import geodesic
from geopy import Nominatim
import time
import os

def possiblelocations(url, xlsx):
    response = requests.get(url)
    if response.status_code == 200: #200 is response code of "OK"
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'class': 'wikitable'})#Wikipedia tables' are generally classified as wikitable

        #Find all table rows
        rows = table.find_all('tr')
        
        data = []
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all(['th', 'td']) #Table header, table data
            city_name = columns[0].text.strip() #Turn the col0 cities into text
            country = columns[1].text.strip()
            data.append([city_name, country])
    data.remove(data[0])
    data.remove(['', ''])
    countrylist = []
    dummylist = copy.deepcopy(data)  # use copy module to make a safe copy

    for i in data:
        if i[1] not in countrylist:
            countrylist.append(i[1])
        else:
            dummylist.remove(i)

    data = dummylist #The repeated countries has removed. We onnly have non-repeated ones now
    cities = [item[0] for item in data] #to more appropriate coordinates only city names are taken
    city_combinations = []
    city_combinations = [[i, j] for i in cities for j in cities] #A combination of cities has made

    #to define data set column names
    df = pd.DataFrame(city_combinations, columns=["C1","C2"])

    df.to_excel(xlsx, index=False)
    print('Saved succesfully to', xlsx)

    #Now we have found the most crowded regions and combinations as possible supply and demand locations

    df = pd.DataFrame(data, columns=["City", "Country"])

    #Create a list based on unique countries.
    unique_countries = df["Country"].unique()

def getcoordinates(xlsx,xlsx2):

    # read the excel file
    excel_file_path = xlsx
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
    df_coordinates.to_excel(xlsx2, index=False)
    print('Saved Succesfully to',xlsx2)

#Here is the function for calculating the distance
def dist(c1,c2):
    return geodesic(c1,c2).kilometers

def getdistance(xlsx,xlsx2):
    #read data from two previous 
    citiescombinations_df = pd.read_excel(xlsx)
    singledist_df = pd.read_excel(xlsx2)

    city_combinations = citiescombinations_df[["C1", "C2"]]
    newdata = {}
    for index, row in city_combinations.iterrows():
        city1 = row["C1"]
        coord1 = singledist_df[singledist_df['Countries'] == city1].iloc[0,1]
        coord_tuple1 = tuple(map(float, coord1.strip('()').split(', ')))
        
        city2 = row["C2"]
        coord2 = singledist_df[singledist_df['Countries'] == city2].iloc[0,1]
        coord_tuple2 = tuple(map(float, coord2.strip('()').split(', ')))
        newdata[city1+city2] = dist(coord_tuple1,coord_tuple2)
    newdata=list(newdata.values())

    citiescombinations_df.insert(2, "Distances", newdata , True)
    print(citiescombinations_df)
    print("Distance data is ready to use")
    os.remove(xlsx)
    citiescombinations_df.to_excel(xlsx, index=True)

start =time.time()
possiblelocations('https://en.wikipedia.org/wiki/List_of_largest_cities', 'largest_cities.xlsx')
getcoordinates("largest_cities.xlsx", "CitiesCoordinates.xlsx")
getdistance("largest_cities.xlsx", "CitiesCoordinates.xlsx")
end = time.time()
print(end-start)
