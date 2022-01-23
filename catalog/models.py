from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Cocktails(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100, help_text='What is the name of this cocktail')

    alcoholic = models.BooleanField(default=True)

    training = models.BooleanField(default=False)

    #glass = models.CharField(max_length=100, null=True, blank=True)
    #unecessary for now

    def __str__(self):
        """String for representing the Model object."""
        return self.name

#for now we are not going to include the tools you would need since we are not making instructions yet
# class Tools(models.Model):
#     tool_id = models.AutoField(primary_key=True)

#     tool_name = models.CharField(max_length=100)

#     tool_description = models.CharField(max_length=500, null=True, blank=True)

#     #type of Tools: shaker, cocktail shaker, strainer, ...

#     def __str__(self): 
#         """String for representing the Model object."""
#         return self.tool_name

class Ingredients(models.Model):
    TYPE_CHOICES = (
        ('alcohol', 'Alcohol'),
        ('mixer', 'Mixer'),
        ('modifier', 'Modifier'),
    )

    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100, null=True, blank=True)

    alcoholic = models.BooleanField(default=True)

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='alcohol')

    category = models.CharField(max_length=100, null=True, blank=True)

    #ingredient_description = models.CharField(max_length=500, null=True, blank=True)
    #no need for this yet

    def __type__(self):
        """String for representing the Model object."""
        return str(self.type)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Measurements(models.Model):
    id = models.AutoField(primary_key=True)

    original_measurement = models.CharField(max_length=20, null=True, blank=True)

    amount_ounces = models.FloatField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.amount_ounces)

    
class RecipeSteps(models.Model):
    id = models.AutoField(primary_key=True)

    cocktail = models.ForeignKey('Cocktails', on_delete=models.SET_NULL, null=True)

    ingredient = models.ForeignKey('Ingredients', on_delete=models.SET_NULL, null=True)

    measurement = models.ForeignKey('Measurements', on_delete=models.SET_NULL, null=True)

    # step_number = models.IntegerField()
    
    # step_description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        returnString = str(self.measurement) + " ounces of " + str(self.ingredient)
        return str(returnString)

class ChromosomeDB(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100, null=True, blank=True)

    population = models.ForeignKey('Population', on_delete=models.SET_NULL, null=True)

    rating = models.IntegerField(default = 5)


class Gene(models.Model):
    id = models.AutoField(primary_key=True)

    chromosomeDB = models.ForeignKey('ChromosomeDB', on_delete=models.SET_NULL, null=True)

    ingredient = models.ForeignKey('Ingredients', on_delete=models.SET_NULL, null=True)

    amount = models.ForeignKey('Measurements', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.amount) + str(self.ingredient)

class Population(models.Model):
    id = models.AutoField(primary_key=True)

    # training = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class AvailableIngredients(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    ingredient = models.ForeignKey('Ingredients', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        returnString = str(self.user.username) + " has " + str(self.ingredient)
        return str(returnString)