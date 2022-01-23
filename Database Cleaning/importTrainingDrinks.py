import json
import requests
import re
from fractions import Fraction
from types import SimpleNamespace


def main():
    l = 471
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    allDrinks = loadData(l)
    cocktails = []
    ingredients = []
    recipes = {}
    normalIngredients = getNormalIngredients()
    i = 35
    # for section in allDrinks:
    #     l += len(section)
    for section in allDrinks:
        for drink in section:
            cocktails, ingredients, recipes = extractData(drink, cocktails, ingredients, recipes, normalIngredients)
            i+=1
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    # l += len(ingredients)
    return cocktails, recipes 

def getNormalIngredients():
    f = open("normalIngredients.txt", "r")
    lines = f.readlines()
    normalIngredients = []
    for line in lines:
        ingredient = ""
        words = line.split(" ")
        for word in words:
            if word == "type:":
                break
            ingredient += word + " "
        normalIngredients.append(ingredient.strip())

    return normalIngredients

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


def extractData(drink, cocktails, ingredients, recipes, normalIngredients): #get the data from each drink in more usable form
    drink = json.loads(drink) #reload the json as a object that python can parse
    newCocktails = []
    newIngredients = []
    newRecipes = []    
    newCocktails, newIngredients, newRecipes = cleanDrink(drink, cocktails, ingredients, recipes, normalIngredients)
    if newCocktails and newIngredients and newRecipes:
        return newCocktails, newIngredients, newRecipes
    else:
        return cocktails, ingredients, recipes
        
 
def cleanDrink(drink, cocktails, ingredients, recipes, normalIngredients): #take each drink and extract the necessary info we need to feed it into the database
    drinkType = drink["strCategory"]
    if not drinkType:
        drinkType = "null"
    drinkName = drink["strDrink"].strip("\'\"").lower()
    if not drinkName in ["abilene", "bloody mary", "cuba libra", "cream soda", "caipirissima", "daiquiri", "dragonfly", "dark and stormy", "espresso martini", "frozen mint daiquiri", "frozen pineapple daiquiri", "gimlet", "gin fizz", "gin sling", "gin smash", "gin toddy", "greyhound", "grass skirt", "honey bee", "hot toddy", "happy skipper", "havana cocktail", "hawaiian cocktail", "ipamena", "ice pick", "irish russian", "jitterbug", "jello shots", "kamikaze", "kiwi martini", "kool-aid slammer", "long island tea", "mojito", "margarita", "mint julep", "moscow mule", "munich mule", "mango mojito", "monkey wrench", "orange whip", "orange crush", "oreo mudslide", "orange push-up", "paloma", "pineapple paloma", "pink panty pulldowns", "passion fruit martini", "quentin", "rum toddy", "rum screwdriver", "sangria", "salty dog", "sea breeze", "scotch sour", "screwdriver", "tequila sour", "tequila sunrise", "tequila slammer", "vampiro", "van vleet", "vodka fizz", "victory collins", "vodka and tonic", "white lady", "white russian", "winter paloma"]:
        return None, None, None
    alcoholic = drink["strAlcoholic"]
    drinkIngredients = [] #ingredients and measurements that are specific to this drink
    drinkMeasurements = []
    badIngredient = False
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
        if ingredient and ingredient.strip().lower() not in normalIngredients:
            badIngredient = True
            break
        if  ingredient:
            if measurement:
                parsedMeasure = parseMeasurement(measurement)
                drinkMeasurements.append(parsedMeasure)
            else:
                drinkMeasurements.append("")
            drinkIngredients.append(ingredient.strip().lower())
            if ingredient.strip().lower() not in ingredients:
                ingredients.append(ingredient.strip().lower())
        j+=1
    if not badIngredient:
        cocktails.append(drinkName)
        recipes[drinkName] = (drinkType, alcoholic, drinkIngredients, drinkMeasurements)
        return cocktails, ingredients, recipes
    else:
        return None, None, None


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
    originalmeasurement = numberstr
    unitstr += measurement.strip().lower()
    originalunit = unitstr
    numberstr = numify(numberstr)
    convertedNum, unit = convertToOz(unitstr, numberstr)
    parsedMeasure = str(convertedNum) + " " + str(unit) + ",  " + str(originalmeasurement) + " " + str(originalunit)
    print(originalunit)
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
    if measurementstr == 'oz' or measurementstr =='fl oz' or measurementstr =='jigger' or measurementstr =='jiggers': #convert standard other measurements to fluid ounces
        convertedNum = num
    elif measurementstr =='tsp':
        convertedNum = num/6
    elif measurementstr =='tblsp':
        convertedNum = num/2
    elif measurementstr =='cup' or measurementstr =='cups':
        convertedNum = num*8
    elif measurementstr =='shots' or measurementstr =='shot':
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
        return num, measurementstr
    unit = "oz"
    return convertedNum, unit
    
           
#print("there are", numDrinks, "cocktails in the database")
# print("here are all the drinks", cocktails)
# print("here are all the ingredients")
# for ingredient in ingredients:
#     print(ingredient)

# importAllDrinksMain()