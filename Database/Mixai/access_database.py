import os
import django

from Mixai.wsgi import *
from catalog.models import Cocktails, Ingredients, RecipeSteps, Tools, Measurements

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mixai.settings')
django.setup()

# Access model field values using Python attributes.
cocktails_list = Cocktails.objects.all()
Ingredients_list = RecipeSteps.objects.filter(cocktail = 4)
print(cocktails_list) # should return 1 for the first record.
print(Ingredients_list)

