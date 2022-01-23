import os
import django
from importNormalDrinks import main as normalDrinksMain
from Mixai.wsgi import *
from catalog.models import Cocktails, Ingredients, RecipeSteps, Measurements

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mixai.settings')
django.setup()

def main():
    importedCocktails, importedRecipes = normalDrinksMain()
    allRecipes = makeRecipes(importedCocktails, importedRecipes)
    writeToFile(allRecipes)


def writeToFile(allRecipes):
    f = open("normalRecipes.txt", "w")
    for recipe in allRecipes:
        if recipe:
            f.write(recipe[0][2]+":")
            f.write("(" + recipe[0][1] + ", " + recipe[0][0] + ")")
            f.write('\n')
        for step in recipe:
            for part in step[3:]:
                f.write(part + " ")
            f.write('\n')
        f.write('\n')
    f.close()

def makeRecipes(importedCocktails, importedRecipes):
    allRecipes = []
    for drink in importedCocktails:
        recipe = []
        drinkType = importedRecipes[drink][0]
        alcoholic = importedRecipes[drink][1]
        if not drinkType:
            drinkType = ""
        if not alcoholic:
            alcoholic = ""
        drinkIngredients = importedRecipes[drink][2]
        drinkMeasurements = importedRecipes[drink][3]
        for i in range(len(drinkIngredients)):
            curIngredient = drinkIngredients[i]
            curMeasurement = drinkMeasurements[i]
            recipeStepToAdd = (alcoholic, drinkType, drink, curIngredient, curMeasurement)
            recipe.append(recipeStepToAdd)
        allRecipes.append(recipe)
    return allRecipes


main()

# # Create a new record using the model's constructor.
# record = MyModelName(my_field_name="Instance #1")

# # Save the object into the database.
# record.save()

# # Access model field values using Python attributes.
# print(record.id) # should return 1 for the first record.
# print(record.my_field_name) # should print 'Instance #1'

# # Change record by modifying the fields, then calling save().
# record.my_field_name = "New Instance Name"
# record.save()


# all_books = Book.objects.all()

# wild_books = Book.objects.filter(title__contains='wild')
# number_wild_books = wild_books.count()