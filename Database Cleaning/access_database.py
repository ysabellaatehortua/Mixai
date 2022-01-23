import os
import django

from Mixai.wsgi import *
from catalog.models import Cocktails, Ingredients, RecipeSteps, Measurements

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mixai.settings')
django.setup()

# Access model field values using Python attributes.
#Ingredients_list = RecipeSteps.objects.filter(cocktail = 4)
#print(Ingredients_list)


#get list of all recipies
# recipe_list = list(RecipeSteps.objects.all())
# for recipe in recipe_list:
#     print(recipe)

#get specific recipe of a cocktail
scooter_obj = Cocktails.objects.get(cocktail_name = 'scooter')
scooter_ingredients = RecipeSteps.objects.filter(cocktail = scooter_obj)
for step in scooter_ingredients:
    print(step)


#print out list of all cocktails
# cocktails_list = list(Cocktails.objects.all())
# for cocktail in cocktails_list:
#     print(cocktail)