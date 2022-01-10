from django.contrib import admin

from .models import Cocktails, Ingredients, RecipeSteps, Measurements

# Register your models here.

admin.site.register(Cocktails)
admin.site.register(Ingredients)
admin.site.register(RecipeSteps)
admin.site.register(Measurements)