import os
import django

from Mixai.wsgi import *
from catalog.models import Cocktails, Ingredients, RecipeSteps, Tools, Measurements

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mixai.settings')
django.setup()

drink1 = Cocktails(cocktail_name = "Mojito", alcoholic = True)

ingredient1 = Ingredients(ingredient_name = "light rum")
ingredient2 = Ingredients(ingredient_name = "lime juice")
ingredient3 = Ingredients(ingredient_name = "sugar")
ingredient4 = Ingredients(ingredient_name = "mint")
ingredient5 = Ingredients(ingredient_name = "soda water")

Measurement1 = Measurements(measurement_name = "ounce", quantity = 2, num_ounces = 0) #rum
Measurement2 = Measurements(measurement_name = "ounce", quantity = 1, num_ounces = 0) #lime
Measurement3 = Measurements(measurement_name = "ounce", quantity = .33, num_ounces = 0) #sugar
Measurement4 = Measurements(measurement_name = "whole", quantity = 3, num_ounces = 0) #mint
Measurement5 = Measurements(measurement_name = "ounce", quantity = 4, num_ounces = 0) #soda water

recipeStep1 = RecipeSteps(cocktail = drink1, ingredient = ingredient1, measurement = Measurement1, step_number = 1)
recipeStep2 = RecipeSteps(cocktail = drink1, ingredient = ingredient2, measurement = Measurement2, step_number = 2)
recipeStep3 = RecipeSteps(cocktail = drink1, ingredient = ingredient3, measurement = Measurement3, step_number = 3)
recipeStep4 = RecipeSteps(cocktail = drink1, ingredient = ingredient4, measurement = Measurement4, step_number = 4)
recipeStep5 = RecipeSteps(cocktail = drink1, ingredient = ingredient5, measurement = Measurement5, step_number = 5)

drink1.save()

ingredient1.save()
ingredient2.save()
ingredient3.save()
ingredient4.save()
ingredient5.save()

Measurement1.save()
Measurement2.save()
Measurement3.save()
Measurement4.save()
Measurement5.save()

recipeStep1.save()
recipeStep2.save()
recipeStep3.save()
recipeStep4.save()
recipeStep5.save()


drink2 = Cocktails(cocktail_name = "Mojito", alcoholic = True)

ingredient1 = Ingredients(ingredient_name = "light rum")
ingredient2 = Ingredients(ingredient_name = "lime juice")
ingredient3 = Ingredients(ingredient_name = "sugar")
ingredient4 = Ingredients(ingredient_name = "mint")
ingredient5 = Ingredients(ingredient_name = "soda water")

Measurement1 = Measurements(measurement_name = "ounce", quantity = 2, num_ounces = 0) #rum
Measurement2 = Measurements(measurement_name = "ounce", quantity = 1, num_ounces = 0) #lime
Measurement3 = Measurements(measurement_name = "ounce", quantity = .33, num_ounces = 0) #sugar
Measurement4 = Measurements(measurement_name = "whole", quantity = 3, num_ounces = 0) #mint
Measurement5 = Measurements(measurement_name = "ounce", quantity = 4, num_ounces = 0) #soda water

recipeStep1 = RecipeSteps(cocktail = drink1, ingredient = ingredient1, measurement = Measurement1, step_number = 1)
recipeStep2 = RecipeSteps(cocktail = drink1, ingredient = ingredient2, measurement = Measurement2, step_number = 2)
recipeStep3 = RecipeSteps(cocktail = drink1, ingredient = ingredient3, measurement = Measurement3, step_number = 3)
recipeStep4 = RecipeSteps(cocktail = drink1, ingredient = ingredient4, measurement = Measurement4, step_number = 4)
recipeStep5 = RecipeSteps(cocktail = drink1, ingredient = ingredient5, measurement = Measurement5, step_number = 5)

drink1.save()

ingredient1.save()
ingredient2.save()
ingredient3.save()
ingredient4.save()
ingredient5.save()

Measurement1.save()
Measurement2.save()
Measurement3.save()
Measurement4.save()
Measurement5.save()

recipeStep1.save()
recipeStep2.save()
recipeStep3.save()
recipeStep4.save()
recipeStep5.save()



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