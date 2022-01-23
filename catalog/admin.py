from django.contrib import admin

from .models import Cocktails, Ingredients, RecipeSteps, Measurements, AvailableIngredients, ChromosomeDB, Gene

# Register your models here.

admin.site.register(Cocktails)
admin.site.register(Ingredients)
admin.site.register(RecipeSteps)
admin.site.register(Measurements)
admin.site.register(AvailableIngredients)
admin.site.register(ChromosomeDB)
admin.site.register(Gene)