import json
import requests


numDrinks = 0
for char in "1234567890abcdefghijklmnopqrstuvwxyz":
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?f="+char)
    drinks = json.loads(response.text)
    if drinks["drinks"]:
        for i in range(len(drinks["drinks"])):
            print(json.dumps(drinks["drinks"][i]["strDrink"]))
            numDrinks+=1
print("there are", numDrinks, "cocktails in the database")