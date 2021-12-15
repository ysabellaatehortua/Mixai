from django.db import models
import uuid

# Create your models here.

class Cocktails(models.Model):
    cocktail_id = models.AutoField(primary_key=True)

    cocktail_name = models.CharField(max_length=100, help_text='What is the name of this cocktail')

    alcoholic = models.BooleanField()

    def __str__(self):
        """String for representing the Model object."""
        return self.cocktail_name


class Tools(models.Model):
    tool_id = models.AutoField(primary_key=True)

    tool_name = models.CharField(max_length=100)

    tool_description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.tool_name



class Ingredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True)

    ingredient_name = models.CharField(max_length=100)

    ingredient_description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.ingredient_name


class Measurements(models.Model):
    measurement_id = models.AutoField(primary_key=True)

    measurement_name = models.CharField(max_length=100)

    quantity = models.FloatField()

    num_ounces = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.quantity

    
class RecipeSteps(models.Model):
    recipe_steps_id = models.AutoField(primary_key=True)

    cocktail = models.ForeignKey('Cocktails', on_delete=models.SET_NULL, null=True)

    tool = models.ForeignKey('Tools', on_delete=models.SET_NULL, null=True)

    ingredient = models.ForeignKey('Ingredients', on_delete=models.SET_NULL, null=True)

    measurement = models.ForeignKey('Measurements', on_delete=models.SET_NULL, null=True)

    step_number = models.IntegerField()
    
    step_description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.step_description