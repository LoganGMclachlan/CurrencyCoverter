import json
from urllib.request import urlopen

# gets exchange rate data
with urlopen("http://www.floatrates.com/daily/gbp.json") as response:
    source = response.read()
data = json.loads(source)

# initialises the list of currancies
currancies = []

# adds the items from exchange rate data to a list
for item in data:
    currancies.append(item)

# loop for each currancy in list
for i in range(0,len(data)):
    # calculates the space between currancy name and code based on name length
    spacing = " "
    length = 40 - len(data[currancies[i]]["name"])
    for space in range(0,length):
        spacing += " "

    # outputs the name and code for each currancy
    print("Name: " + data[currancies[i]]["name"] + spacing + "Code: " + data[currancies[i]]["code"])

# holds open terminal
__v = input("")