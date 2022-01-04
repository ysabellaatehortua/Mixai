import json
import requests
import re
from types import SimpleNamespace


def main():
    allDrinks = loadData()
    cocktails = []
    ingredients = []
    for section in allDrinks:
        for drink in section:
            # print(drink)
            # print()
            # print()
            cocktails, ingredients = extractData(drink, cocktails, ingredients)

def loadData(): #get json data from website
    allDrinks = []
    for char in "1234567890abcdefghijklmnopqrstuvwxyz":
        section = []
        response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?f="+char)
        drinks = json.loads(response.text)
        if drinks["drinks"]: 
            for i in range(len(drinks["drinks"])):
                newDrinks = json.dumps(drinks["drinks"][i]) #store in sections for each letter
                section += [newDrinks]
        allDrinks += [section]
    return allDrinks


def extractData(drink, cocktails, ingredients): #get the data from each drink in more usable form
    newCocktails = [] 
    newIngredients = []
    drink = json.loads(drink)
    drinkType = drink["strCategory"] #make sure the type is not a shot or coffee or other weird drink for now
    if (drinkType == "Cocktail" or drinkType == "Ordinary Drink" or drinkType == "Punch / Party Drink"):
        cleanedDrink = cleanDrink(drink, ingredients)
    cocktails += newCocktails
    ingredients += newIngredients
    return cocktails, ingredients
 
def cleanDrink(drink, ingredients): #take each drink and extract the necessary info we need to feed it into the database
    drinkName = drink["strDrink"].strip("\'\"").lower
    alcoholic = (drink["strAlcoholic"] == "\"Alcoholic\"")
    glass = drink["strGlass"]
    measurements = []
    done = False
    j = 1
    while not done and j < 16: #loop through all possible ingredients
        ingredientString = "strIngredient"+str(j)
        measurementString = "strMeasure"+str(j)
        ingredient = drink[ingredientString]
        measurement = drink[measurementString] #seperate ingredient and measurement and clean them both 
        if ingredient == "null" or ingredient == "":
            done = True
            continue
        if measurement and ingredient:
            # measurements += parseMeasurement(measurement)
            parseMeasurement(measurement)
            ingredients += (ingredient)
        j+=1
    newDrink = {drinkName : [alcoholic, glass, [ingredients], [measurements]]}
    return newDrink
    

def parseMeasurement(measure): #this will be more or less what is done in testMeasurements
    print(measure)
    # quantity = 0
    # unit = ""
    # cleanedMeasure = (quantity, unit) 
    # numberstr = re.search("^[0-9].*[0-9]$", measure)
    # print(numberstr)
    # return cleanedMeasure
    
           
#print("there are", numDrinks, "cocktails in the database")
# print("here are all the drinks", cocktails)
# print("here are all the ingredients")
# for ingredient in ingredients:
#     print(ingredient)

main()