import json
import requests
import re
from fractions import Fraction
from types import SimpleNamespace


def importAllDrinksMain():
    l = 766
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    allDrinks = loadData(l)
    cocktails = []
    ingredients = []
    recipes = {}
    i = 35
    # for section in allDrinks:
    #     l += len(section)
    for section in allDrinks:
        for drink in section:
            cocktails, ingredients, recipes = extractData(drink, cocktails, ingredients, recipes)
            i+=1
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    # l += len(ingredients)
    print("there are", len(ingredients), "ingredients")
    ingredientObjects = getIngredientData(ingredients, i, l)
    return cocktails, ingredientObjects, recipes 

def loadData(l): #get json data from website
    allDrinks = []
    i = 0
    for char in "1234567890abcdefghijklmnopqrstuvwxyz":
        printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        section = []
        response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?f="+char)
        drinks = json.loads(response.text)
        if drinks["drinks"]: 
            for i in range(len(drinks["drinks"])):
                newDrinks = json.dumps(drinks["drinks"][i]) #store in sections for each letter
                section += [newDrinks]
        allDrinks += [section]
        i += 1
    return allDrinks


def getIngredientData(ingredients, i, l): #get json data from website
    ingredientObjects = []
    for ingredient in ingredients:
        printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?i="+ingredient)
        ingredientData = json.loads(response.text)["ingredients"][0]
        type = ingredientData["strType"]
        name = ingredient
        alcohol = ingredientData["strAlcohol"]
        abv = ingredientData["strABV"]
        newIngredient = (name, type, alcohol, abv)
        ingredientObjects.append(newIngredient)
        i += 1
    return ingredientObjects


def extractData(drink, cocktails, ingredients, recipes): #get the data from each drink in more usable form
    drink = json.loads(drink) #reload the json as a object that python can parse
    newCocktails = []
    newIngredients = []
    newRecipes = []    
    newCocktails, newIngredients, newRecipes = cleanDrink(drink, cocktails, ingredients, recipes)
    if newCocktails and newIngredients and newRecipes:
        return newCocktails, newIngredients, newRecipes
    else:
        return cocktails, ingredients, recipes
        
 
def cleanDrink(drink, cocktails, ingredients, recipes): #take each drink and extract the necessary info we need to feed it into the database
    drinkType = drink["strCategory"]
    if not drinkType:
        drinkType = "null"
    drinkName = drink["strDrink"].strip("\'\"").lower()
    alcoholic = (drink["strAlcoholic"] == "\"Alcoholic\"")
    drinkIngredients = [] #ingredients and measurements that are specific to this drink
    drinkMeasurements = []
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
            drinkMeasurements.append(measurement)
            drinkIngredients.append(ingredient.strip().lower())
            if ingredient.strip().lower() not in ingredients:
                ingredients.append(ingredient.strip().lower())
        j+=1
    cocktails.append(drinkName)
    recipes[drinkName] = (drinkType, alcoholic, drinkIngredients, drinkMeasurements)
    return cocktails, ingredients, recipes


    # Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    suffix = str(iteration) + "/" + str(total) 
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
    
           
#print("there are", numDrinks, "cocktails in the database")
# print("here are all the drinks", cocktails)
# print("here are all the ingredients")
# for ingredient in ingredients:
#     print(ingredient)

# importAllDrinksMain()