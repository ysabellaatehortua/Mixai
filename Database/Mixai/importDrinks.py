import json
import requests
import re
from fractions import Fraction
from types import SimpleNamespace


def main():
    allDrinks = loadData()
    cocktails = []
    ingredients = []
    measurements = []
    recipes = {}
    for section in allDrinks:
        for drink in section:
            cocktails, ingredients, measurements, recipes = extractData(drink, cocktails, ingredients, measurements, recipes)
    # for drink in cocktails:
    #     print(drink, recipes[drink])
    return cocktails, ingredients, measurements, recipes

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


def extractData(drink, cocktails, ingredients, measurements, recipes): #get the data from each drink in more usable form
    drink = json.loads(drink) #reload the json as a object that python can parse
    drinkType = drink["strCategory"] #make sure the type is not a shot or coffee or other weird drink for now
    newCocktails = []
    newIngredients = []
    newMeasurements = []
    newRecipes = []    
    if (drinkType == "Cocktail" or drinkType == "Ordinary Drink" or drinkType == "Punch / Party Drink"):
        newCocktails, newIngredients, newMeasurements, newRecipes = cleanDrink(drink, cocktails, ingredients, measurements, recipes)
    if newCocktails and newIngredients and newMeasurements and newRecipes:
        return newCocktails, newIngredients, newMeasurements, newRecipes
    else:
        return cocktails, ingredients, measurements, recipes
        
 
def cleanDrink(drink, cocktails, ingredients, measurements, recipes): #take each drink and extract the necessary info we need to feed it into the database
    drinkName = drink["strDrink"].strip("\'\"").lower()
    alcoholic = (drink["strAlcoholic"] == "\"Alcoholic\"")
    glass = drink["strGlass"]
    drinkIngredients = [] #ingredients and measurements that are specific to this drink
    drinkMeasurements = [] #in form of [measurement in ounces, 'oz', measurement in original units, original units]
    badMeasurement = False
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
            measurementName = getMeasureName(measurement)
            knownMeasurements = ["oz", "floz", "tsp", 'tblsp', 'cup', 'cups', 'shots', 'shot', 'jigger', 'jiggers', 'pint', 'pints', 'qt', 'cl', 'ml', 'dl', 'gr', 'L', 'gal', 'lb', 'can']
            if measurementName not in knownMeasurements:
                badMeasurement = True
                break
            parsedMeasure = parseMeasurement(measurement)
            drinkMeasurements.append(parsedMeasure)
            drinkIngredients.append(ingredient)
            if parsedMeasure not in measurements: #check if measurement and ingredient already present in list of all ingredients or measures
                measurements.append(parsedMeasure)
            if ingredient not in ingredients:
                ingredients.append(ingredient)
        j+=1
    if not badMeasurement and drinkName not in cocktails:
        cocktails.append(drinkName)
        #newDrink = {drinkName : (alcoholic, glass, [drinkIngredients], [drinkMeasurements])}
        #recipes.update(newDrink)
        recipes[drinkName]= (alcoholic, glass, drinkIngredients, drinkMeasurements)
        return cocktails, ingredients, measurements, recipes
    else:
        return None, None, None, None

def getMeasureName(measurement):
    toRemove = " 0123456789/-.\""
    measurement = measurement.replace(" or ", '')
    for char in toRemove:
        measurement = measurement.replace(char, '')
    measurement = measurement.lower()
    return measurement
    

def parseMeasurement(measurement):
    originalunit = ""
    originalmeasurement = ""
    numberstr = "" 
    unitstr = ""
    done = True in [char.isdigit() for char in measurement] #check if there are more numbers left in the measurement
    seenNum = False
    while done: #split the number of the measurement from the unit of the measurement
        if measurement[0].isdigit(): #check if we have seen a digit yet (in case the number is after the measurement)
            seenNum = True
        if seenNum:
            numberstr += measurement[0]
            measurement = measurement[1:]
        else:
            unitstr += measurement[0].strip().lower()
            measurement = measurement[1:]
        done = True in [char.isdigit() for char in measurement]
    originalunit = unitstr
    originalmeasurement = numberstr
    unitstr += measurement.strip().lower()
    numberstr = numify(numberstr)
    convertedNum, unit = convertToOz(unitstr, numberstr)
    parsedMeasure = (convertedNum, unit, originalmeasurement, originalunit)
    return parsedMeasure



def numify(measurementnum): 
    if measurementnum == "70ml/2": #annoying edge case
        num = 2
    elif '/' in measurementnum:
        num = float(sum(Fraction(s) for s in measurementnum.split())) #deal with different ways strings represent numbers 
    elif '.' in measurementnum:
        num = float(measurementnum)
    elif '-' in measurementnum:
        a,b = measurementnum.split("-")
        num = float((int(a)+int(b))/2)
    elif 'or' in measurementnum:
        a,b = measurementnum.split("or")
        num = float((int(a)+int(b))/2)
    elif measurementnum == '':
        num = ''
    else:
        num = float(measurementnum)
    return num

def convertToOz(measurementstr, num):
    if measurementstr == 'oz' or measurementstr =='fl oz': #convert standard other measurements to fluid ounces
        convertedNum = num
    elif measurementstr =='tsp':
        convertedNum = num/6
    elif measurementstr =='tblsp':
        convertedNum = num/2
    elif measurementstr =='cup' or measurementstr =='cups':
        convertedNum = num*8
    elif measurementstr =='shots' or measurementstr =='shot' or measurementstr =='jigger' or measurementstr =='jiggers':
        convertedNum = num*1.5
    elif measurementstr =='pint' or measurementstr =='pints':
        convertedNum = num*16
    elif measurementstr =='qt':
        convertedNum = num*32
    elif measurementstr =='cl':
        convertedNum = num/2.957
    elif measurementstr =='ml':
        convertedNum = num/29.574
    elif measurementstr =='dl':
        convertedNum = num*3.381
    elif measurementstr =='gr':
        convertedNum = num/29.574
    elif measurementstr =='L':
        convertedNum = num*33.814
    elif measurementstr =='gal':
        convertedNum = num*128
    elif measurementstr =='lb':
        convertedNum = num*15.34
    elif measurementstr =='can':
        convertedNum = num*12
    else:
        return "null"
    unit = "oz"
    return convertedNum, unit
    
           
#print("there are", numDrinks, "cocktails in the database")
# print("here are all the drinks", cocktails)
# print("here are all the ingredients")
# for ingredient in ingredients:
#     print(ingredient)

main()