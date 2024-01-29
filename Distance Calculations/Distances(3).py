import pandas as pd
from geopy.distance import geodesic

#Here is the function for calculating the distance
def dist(c1,c2):
    return geodesic(c1,c2).kilometers

#read data from two previous 
citiescombinations_df = pd.read_excel("largest_cities.xlsx")
singledist_df = pd.read_excel("CitiesCoordinates.xlsx")

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

import os
os.remove("largest_cities.xlsx")
citiescombinations_df.to_excel("largest_cities.xlsx", index=True)

