from django.shortcuts import render
from django.contrib.auth.models import User
import create_training_data
from geneticAlgorithmDB import GeneticAlgorithm
from .models import AvailableIngredients, Cocktails, Ingredients, RecipeSteps, Measurements, ChromosomeDB, Gene


# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    # num_cocktails = Cocktails.objects.all().count()

    # # The 'all()' is implied by default.
    # num_ingredients = Ingredients.objects.count()

    available_ingredients = AvailableIngredients.objects.all()

    all_ingredients = Ingredients.objects.all()

    # if request.user.is_authenticated():
    #     username = request.user.username
    if request.method == 'POST':
        for ingredient in all_ingredients:
            if request.POST.get(ingredient.name) and not AvailableIngredients.objects.filter(ingredient = ingredient).exists():
                newAvailableIngredients = AvailableIngredients(user = request.user, ingredient = ingredient)
                newAvailableIngredients.save()

    context = {
        # 'num_cocktails': num_cocktails,
        # 'num_ingredients': num_ingredients,
        'available_ingredients': available_ingredients
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def genetic_alg(request):

    create_training_data.main(user = request.user)

    available_ingredients = AvailableIngredients.objects.all()

    gen_alg = GeneticAlgorithm(user = request.user)
    gen_alg.create_fitness_func()
    gen_alg.gen_alg()
    output_chromosomes = ChromosomeDB.objects.filter(population = gen_alg.training_population)
    print("output_chromosomes", output_chromosomes)
    for i in range(min( 25, len(output_chromosomes))):#range(len(gen_alg.population)):
        chromosome = output_chromosomes[i]
        genes = Gene.objects.filter(chromosomeDB = chromosome)
        print(chromosome.name)
        for gene in genes:
            print(gene)
        print(gen_alg.train_output[i])
        print('\n')

    context = {
        'available_ingredients': available_ingredients,
        'output_chromosomes' : output_chromosomes
    }


    return render(request, 'genetic_algorithm.html', context=context)