from django.contrib import admin

from .models import Cocktails, Ingredients, RecipeSteps, Tools, Measurements

# Register your models here.

admin.site.register(Cocktails)
admin.site.register(Ingredients)
admin.site.register(RecipeSteps)
admin.site.register(Tools)
admin.site.register(Measurements)