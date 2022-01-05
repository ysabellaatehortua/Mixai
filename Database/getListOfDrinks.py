import json
import requests
import re
from types import SimpleNamespace


def main():
    allIngredients = []
    goodIngredients = []
    goodDrinks = []
    allDrinks = []
    for char in "1234567890abcdefghijklmnopqrstuvwxyz":
        response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?f="+char)
        drinks = json.loads(response.text)
        if drinks["drinks"]: 
            for i in range(len(drinks["drinks"])):
                drinkName = json.dumps(drinks["drinks"][i]["strDrink"])
                allDrinks.append(drinkName)
                badMeasurement = False
                done = False
                j = 1
                while not done and j < 16: #loop through all possible ingredients
                    ingredientString = "strIngredient"+str(j)
                    measurementString = "strMeasure"+str(j)
                    ingredient = json.dumps(drinks["drinks"][i][ingredientString])
                    measurement = json.dumps(drinks["drinks"][i][measurementString])
                    if ingredient == "null" or ingredient == "":
                        done = True
                        continue
                    if measurement and ingredient:
                        allIngredients.append(ingredient)
                        measurementName = getMeasureName(measurement)
                        knownMeasurements = ["oz", "floz", "tsp", 'tblsp', 'cup', 'cups', 'shots', 'shot', 'jigger', 'jiggers', 'pint', 'pints', 'qt', 'cl', 'ml', 'dl', 'gr', 'L', 'gal', 'lb', 'can']
                        if measurementName not in knownMeasurements:
                            badMeasurement = True
                        else:
                            goodIngredients.append(ingredient)
                    j+=1
                if not badMeasurement:
                    goodDrinks.append(drinkName)
               

    writeToFile(allIngredients, goodIngredients, goodDrinks, allDrinks)

            

def getMeasureName(measurement):
    #print("before  ", measurement)
    toRemove = " 0123456789/-.\""
    measurement = measurement.replace(" or ", '')
    for char in toRemove:
        measurement = measurement.replace(char, '')
    measurement = measurement.lower()
    #print("after   ", measurement)
    return measurement

def writeToFile(allIngredients, goodIngredients, goodDrinks, allDrinks):
    f = open("goodDrinks.txt", "w")
    for drink in goodDrinks:
        f.write(drink)
        f.write('\n')
    f.close()
    f = open("allDrinks.txt", "w")
    for drink in allDrinks:
        f.write(drink)
        f.write('\n')
    f.close()
    f = open("goodIngredients.txt", "w")
    for drink in goodIngredients:
        f.write(drink)
        f.write('\n')
    f.close()
    f = open("allIngredients.txt", "w")
    for drink in allIngredients:
        f.write(drink)
        f.write('\n')
    f.close()




main()