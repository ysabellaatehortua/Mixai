import os
import django
from numpy.random import choice, randint
from datetime import time
from Mixai.wsgi import *
from catalog.models import Ingredients, Measurements, Cocktails, RecipeSteps, ChromosomeDB, Gene, Population
from chromosome import Chromosome


def loadIngredients():
    f = open("normalIngredients.txt", "r")
    recipes = {}
    ingredients = {}
    ings = f.readlines()
    for ingredient in ings:
        ingredient = ingredient.rstrip().rsplit('  ')
        if ingredient[2][10:] == 'Yes': #check if ingredient is alcoholic
            newIngredient = Ingredients(name = ingredient[0], alcoholic = True, type = 'alcohol', category = ingredient[1][6:])
            newIngredient.save()
        else:
            if ingredient[1][6:11] == 'Mixer':
                newIngredient = Ingredients(name = ingredient[0], alcoholic = False, type = 'mixer', category = ingredient[1][12:])
                newIngredient.save()
            if ingredient[1][6:14] == 'Modifier':
                newIngredient = Ingredients(name = ingredient[0], alcoholic = False, type = 'modifier', category = ingredient[1][15:])
                newIngredient.save()


def loadTrainingRecipes(user):
    newPopulation = Population(user = user)
    newPopulation.save()
    f = open("convertedTrainingRecipes.txt", "r")
    o = open("train_out.txt", "r")
    training_lines = o.readlines()
    line = f.readline().rstrip()
    i = 0
    while line != '':
        drink = line
        newChromosomeDB = ChromosomeDB(name = drink, population = newPopulation, rating = int(training_lines[i]))
        i+=1
        newChromosomeDB.save()
        line = f.readline()
        while line != '\n' and line != '':
            line = line.rstrip().split('  ')
            ingredient = line[0]
            special = ['Spice', 'Ice', 'Garnish', 'Fruit', 'Unique']
            ingredientObjList = Ingredients.objects.filter(name = ingredient)
            ingredientObj = ingredientObjList[0]
            if ingredientObj.category not in special:
                amt = float(line[1])
            og_amt = line[2]
            type = ingredientObj.type
            newMeasurement = Measurements(original_measurement = og_amt, amount_ounces = amt) #might need to do something to make sure amt is a float
            newMeasurement.save()
            newGene = Gene(chromosomeDB = newChromosomeDB, ingredient = ingredientObj, amount = newMeasurement)
            newGene.save()
            line = f.readline()
        line = f.readline().rstrip()


def main(user):
    loadIngredients()
    loadTrainingRecipes(user)