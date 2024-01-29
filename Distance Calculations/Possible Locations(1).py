import requests
from bs4 import BeautifulSoup
import pandas as pd
import copy


url = 'https://en.wikipedia.org/wiki/List_of_largest_cities'
response = requests.get(url)

if response.status_code == 200: #200 is response code of "OK"
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', {'class': 'wikitable'})#Wikipedia tables' are generally classified as wikitable

    #Find all table rows
    rows = table.find_all('tr')
    
    data = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all(['th', 'td']) #Table header, table data
        city_name = columns[0].text.strip()
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

df.to_excel('largest_cities.xlsx', index=False)
print('Saved succesfully to "largest_cities.xlsx"')

#Now we have found the most crowded regions and combinations as possible supply and demand locations

df = pd.DataFrame(data, columns=["City", "Country"])

# Ülke adlarından benzersiz bir liste oluşturun
unique_countries = df["Country"].unique()
