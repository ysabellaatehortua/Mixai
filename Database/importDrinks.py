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

def loadData():
    allDrinks = []
    for char in "1234567890abcdefghijklmnopqrstuvwxyz":
        section = []
        response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?f="+char)
        drinks = json.loads(response.text)
        if drinks["drinks"]:
            for i in range(len(drinks["drinks"])):
                newDrinks = json.dumps(drinks["drinks"][i])
                section += [newDrinks]
        allDrinks += [section]
    return allDrinks


def extractData(drink, cocktails, ingredients):
    newCocktails = [] 
    newIngredients = []
    drink = json.load(drink)
    drinkType = drink["strCategory"]
    if (drinkType == "\"Cocktail\"" or drinkType == "\"Ordinary Drink\"" or drinkType == "\"Punch / Party Drink\""):
        cleanedDrink = cleanDrink(drink, ingredients)
    cocktails += newCocktails
    ingredients += newIngredients
    return cocktails, ingredients

def cleanDrink(drink, ingredients):
    drinkName = drink["strDrink"].strip("\'\"").lower
    alcoholic = (drink["strAlcoholic"] == "\"Alcoholic\"")
    glass = drink["strGlass"]
    measurements = []
    done = False
    j = 1
    while not done and j < 16:
        ingredientString = "strIngredient"+str(j)
        measurementString = "strMeasure"+str(j)
        ingredient = drink[ingredientString]
        measurement = drink[measurementString]
        if ingredient == "null" or ingredient == "":
            done = True
            continue
        measurements += parseMeasurement(measurement)
        ingredients += (ingredient)
        j+=1
    newDrink = {drinkName : [alcoholic, glass, [ingredients], [measurements]]}
    return newDrink
    

def parseMeasurement(measure):
    quantity = 0
    unit = ""
    cleanedMeasure = (quantity, unit) 
    numberstr = re.search("^[0-9].*[0-9]$", measure)
    print(numberstr)
    return cleanedMeasure
    
           
#print("there are", numDrinks, "cocktails in the database")
# print("here are all the drinks", cocktails)
# print("here are all the ingredients")
# for ingredient in ingredients:
#     print(ingredient)

main()