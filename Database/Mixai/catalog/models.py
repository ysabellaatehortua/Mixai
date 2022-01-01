from django.db import models
import uuid

# Create your models here.

class Cocktails(models.Model):
    cocktail_id = models.AutoField(primary_key=True)

    cocktail_name = models.CharField(max_length=100, help_text='What is the name of this cocktail')

    alcoholic = models.BooleanField(default=True)

    glass = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.cocktail_name


class Tools(models.Model):
    tool_id = models.AutoField(primary_key=True)

    tool_name = models.CharField(max_length=100)

    tool_description = models.CharField(max_length=500, null=True, blank=True)

    #type of Tools: shaker, cocktail shaker, strainer, ...

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


    #types: shot, proportions, oz, tsp, cl, dash, wedge, fill with, part, splash, fresh, parts, tblsp, twist of, dashes, top up, drops, cubes, " ", fifth, small bottle, pint, Juice of, slice, Squeeze, cups, cup, crushed, bottle, dl, gr, Float, fl oz, Pinch, sprigs, stick, ml, qt, piece, Top, can, shots, dashes, glass, chunks, cube, L, Top up with, Garnish, long strip, orange, mini, to taste, fill with, jigger, jiggers, around rim aboout 1 pinch, pinches, (if needed), Turkish apple, Garnish with, inch, gal, lb, chunk, whole, handful, (Claret), Over, scoops, inch strips, Rimmed, Full Glass, Mikey bottle, large bottle, crushed, splashes, cans, Large Sprig, Measures, pods, About 8 Drops, full glass, 

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
        return self.ingredient