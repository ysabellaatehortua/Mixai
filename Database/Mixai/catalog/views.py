from django.shortcuts import render

from .models import Cocktails, Ingredients, RecipeSteps, Tools, Measurements


# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_cocktails = Cocktails.objects.all().count()

    # The 'all()' is implied by default.
    num_ingredients = Ingredients.objects.count()

    context = {
        'num_cocktails': num_cocktails,
        'num_ingredients': num_ingredients
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)