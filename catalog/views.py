from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
import create_training_data
from .forms import NewUserForm
from geneticAlgorithmDB import GeneticAlgorithm
from .models import AvailableIngredients, Cocktails, Ingredients, Population, RecipeSteps, Measurements, ChromosomeDB, Gene


# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    # num_cocktails = Cocktails.objects.all().count()

    # # The 'all()' is implied by default.
    # num_ingredients = Ingredients.objects.count()

    if request.user.is_authenticated:
        if not Population.objects.filter(user = request.user).exists():
            create_training_data.main(user = request.user)
    else:
        return redirect("register")


    available_ingredients = AvailableIngredients.objects.all()

    all_ingredients = Ingredients.objects.all()

    # if request.user.is_authenticated():
    #     username = request.user.username
    if request.method == 'POST':
        for ingredient in all_ingredients:
            if request.POST.get(ingredient.name) and not AvailableIngredients.objects.filter(ingredient = ingredient, user = request.user ).exists():
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

    available_ingredients = AvailableIngredients.objects.all()

    gen_alg = GeneticAlgorithm(user = request.user)
    gen_alg.create_fitness_func()
    gen_alg.gen_alg()
    closest_to_make_output = gen_alg.filter_drinks()
    # closest_to_make = gen_alg.filter_drinks()
    # closest_to_make_genes = Gene.objects.filter(chromosomeDB = closest_to_make)
    # closest_to_make_output = [closest_to_make.name]
    # for gene in closest_to_make_genes:
    #     print(gene)
    #     closest_to_make_output.append(gene)
    output_chromosomes = ChromosomeDB.objects.filter(population = gen_alg.training_population)
    return_chromosome = output_chromosomes[0]
    print(return_chromosome.name)
    to_dispaly = [return_chromosome.name]
    genes = Gene.objects.filter(chromosomeDB = return_chromosome)
    for gene in genes:
        print(gene)
        to_dispaly.append(gene)
    # for i in range(len(output_chromosomes)):#range(len(gen_alg.population)):
    #     same_drink = False
    #     chromosome = output_chromosomes[i]
    #     cur_chromosome = [chromosome.name]
    #     genes = Gene.objects.filter(chromosomeDB = chromosome)
    #     print(chromosome.name)
    #     for gene in genes:
    #         cur_chromosome.append(gene)
    #         print("gene ingredient", gene.ingredient)
    #     for chrom in return_chromosomes:
    #         same_drink = True
    #         for i in range(len(cur_chromosome)-2):
    #             if chrom[i+1].ingredient.name != cur_chromosome[i+1].ingredient.name and chrom[i+1].amount != cur_chromosome[i+1].amount:
    #                 same_drink = False
    #                 break
    #     if not same_drink:
    #         return_chromosomes.append(cur_chromosome)
    #     if len(return_chromosomes) == 5:
    #         break
    #     print()
    #     print(gen_alg.train_output[i])
    #     print('\n')
        

    context = {
        'available_ingredients': available_ingredients,
        'to_dispaly' : to_dispaly,
        'closest_to_make_output' : closest_to_make_output,
    }


    return render(request, 'genetic_algorithm.html', context=context)


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

def about(request):
    return render(request, 'about.html')