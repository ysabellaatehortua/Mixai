from sklearn.linear_model import LinearRegression
import random
import copy 
from django.contrib.auth.models import User
from catalog.models import ChromosomeDB, Gene, Ingredients, Measurements, Population, AvailableIngredients



class GeneticAlgorithm():

    def __init__(self, n = 0, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GeneticAlgorithm, self).__init__(*args, **kwargs)
        self.n = n
        training_populations = Population.objects.filter(user = self.user)
        self.training_population = training_populations[len(training_populations)-1] #get most recent training population for this user
        self.train_input, self.train_output = self.train_input_output_setup()
        self.ingredient_list = {}
        self.simple_types = {}
        self.predictor = LinearRegression(n_jobs=-1)
    

    def train_input_output_setup(self):
        train_input = []
        train_output = []
        population = ChromosomeDB.objects.filter(population = self.training_population)
        for drink in population:
            genes = Gene.objects.filter(chromosomeDB = drink)
            train_output.append(drink.rating)
            total_alc = [0, 0, 0, 0, 0, 0]
            total_mix = [0,0,0,0,0,0,0]
            total_mod = [0,0,0,0,0,0,0,0]
            for gene in genes:
                ingredient_type = gene.ingredient.type
                ingredient_category = gene.ingredient.category
                ingredient_amount = gene.amount.amount_ounces
                if ingredient_type == "alcohol":
                    if ingredient_category == 'Rum':
                        total_alc[0] += ingredient_amount
                    if ingredient_category == 'Spirit':
                        total_alc[1] += ingredient_amount
                    if ingredient_category == 'Whiskey':
                        total_alc[2] += ingredient_amount
                    if ingredient_category == 'Liqueur':
                        total_alc[3] += ingredient_amount
                    if ingredient_category == 'Beer':
                        total_alc[4] += ingredient_amount
                    if ingredient_category == 'Wine':
                        total_alc[5] += ingredient_amount
                if ingredient_type == "mixer":
                    if ingredient_category == 'Juice':
                        total_mix[0] += ingredient_amount
                    if ingredient_category == 'Dairy':
                        total_mix[1] += ingredient_amount
                    if ingredient_category == 'Soda':
                        total_mix[2] += ingredient_amount
                    if ingredient_category == 'Coffee':
                        total_mix[3] += ingredient_amount
                    if ingredient_category == 'Mix':
                        total_mix[4] += ingredient_amount
                    if ingredient_category == 'Water':
                        total_mix[5] += ingredient_amount
                    if ingredient_category == 'Unique':
                        total_mix[6] += ingredient_amount
                if ingredient_type == "modifier":
                    if ingredient_category == 'Bitter':
                        total_mod[0] += ingredient_amount
                    if ingredient_category == 'Fruit':
                        total_mod[1] += ingredient_amount
                    if ingredient_category == 'Sweetner':
                        total_mod[2] += ingredient_amount
                    if ingredient_category == 'Garnish':
                        total_mod[3] += ingredient_amount
                    if ingredient_category == 'Ice':
                        total_mod[4] += ingredient_amount
                    if ingredient_category == 'Sauce':
                        total_mod[5] += ingredient_amount
                    if ingredient_category == 'Spice':
                        total_mod[6] += ingredient_amount
                    if ingredient_category == 'Sour':
                        total_mod[7] += ingredient_amount
            d = total_alc + total_mix + total_mod
            train_input.append(d)
        return train_input, train_output     


    def get_new_train_input(self, population):
        train_input = []
        population = ChromosomeDB.objects.filter(population = population)
        for drink in population:
            genes = Gene.objects.filter(chromosomeDB = drink)
            total_alc = [0, 0, 0, 0, 0, 0]
            total_mix = [0,0,0,0,0,0,0]
            total_mod = [0,0,0,0,0,0,0,0]
            for gene in genes:
                ingredient_type = gene.ingredient.type
                ingredient_category = gene.ingredient.category
                ingredient_amount = gene.amount.amount_ounces
                if ingredient_type == "alcohol":
                    if ingredient_category == 'Rum':
                        total_alc[0] += ingredient_amount
                    if ingredient_category == 'Spirit':
                        total_alc[1] += ingredient_amount
                    if ingredient_category == 'Whiskey':
                        total_alc[2] += ingredient_amount
                    if ingredient_category == 'Liqueur':
                        total_alc[3] += ingredient_amount
                    if ingredient_category == 'Beer':
                        total_alc[4] += ingredient_amount
                    if ingredient_category == 'Wine':
                        total_alc[5] += ingredient_amount
                if ingredient_type == "mixer":
                    if ingredient_category == 'Juice':
                        total_mix[0] += ingredient_amount
                    if ingredient_category == 'Dairy':
                        total_mix[1] += ingredient_amount
                    if ingredient_category == 'Soda':
                        total_mix[2] += ingredient_amount
                    if ingredient_category == 'Coffee':
                        total_mix[3] += ingredient_amount
                    if ingredient_category == 'Mix':
                        total_mix[4] += ingredient_amount
                    if ingredient_category == 'Water':
                        total_mix[5] += ingredient_amount
                    if ingredient_category == 'Unique':
                        total_mix[6] += ingredient_amount
                if ingredient_type == "modifier":
                    if ingredient_category == 'Bitter':
                        total_mod[0] += ingredient_amount
                    if ingredient_category == 'Fruit':
                        total_mod[1] += ingredient_amount
                    if ingredient_category == 'Sweetner':
                        total_mod[2] += ingredient_amount
                    if ingredient_category == 'Garnish':
                        total_mod[3] += ingredient_amount
                    if ingredient_category == 'Ice':
                        total_mod[4] += ingredient_amount
                    if ingredient_category == 'Sauce':
                        total_mod[5] += ingredient_amount
                    if ingredient_category == 'Spice':
                        total_mod[6] += ingredient_amount
                    if ingredient_category == 'Sour':
                        total_mod[7] += ingredient_amount
            d = total_alc + total_mix + total_mod
            train_input.append(d)
        return train_input

        
    def crossover(self, c1, c2, new_population):
        c_new1 = ChromosomeDB(population = new_population)
        c_new2 = ChromosomeDB(population = new_population)

        words1 = c1.name.split()
        words2 = c2.name.split()
        c_new1_name = ""
        c_new2_name = ""
        combo1 = words1[0:int(len(words1)/2)] + words2[int(len(words2)/2):]
        for n in combo1:
            c_new1_name += n
            c_new1_name += " "
        combo2 = words2[0:int(len(words2)/2)] + words1[int(len(words1)/2):]
        for n in combo2:
            c_new2_name += n
            c_new2_name += " "
        c_new1.name = c_new1_name
        c_new2.name = c_new2_name
        c_new1.save()
        c_new2.save()

        all_alcohol = Ingredients.objects.filter(type = 'alcohol')
        all_mixers = Ingredients.objects.filter(type = 'mixer')
        all_modifiers = Ingredients.objects.filter(type = 'modifier')

        new_amount0 = Measurements(amount_ounces = 0)
        new_amount0.save()
        new_amount1 = Measurements(amount_ounces = 1)
        new_amount1.save()
        new_amount2 = Measurements(amount_ounces = 2)
        new_amount2.save()
        new_amount3 = Measurements(amount_ounces = 3)
        new_amount3.save()
        new_amount4 = Measurements(amount_ounces = 4)
        new_amount4.save()
        new_amount5 = Measurements(amount_ounces = 5)
        new_amount5.save()
        new_amount6= Measurements(amount_ounces = 6)
        new_amount6.save()
        amounts = [new_amount0, new_amount1, new_amount2, new_amount3, new_amount4, new_amount4, new_amount6]
        
        c1_alcohol = Gene.objects.filter(chromosomeDB = c1, ingredient__type__contains = 'alcohol')
        c2_alcohol = Gene.objects.filter(chromosomeDB = c2, ingredient__type__contains = 'alcohol')
        alc_crossover = random.randint(0, min(len(c1_alcohol),len(c2_alcohol)))
        for alc in c1_alcohol[:alc_crossover]: #add the first half of the alcohol from gene 1 to new gene 1
            newGene = Gene(chromosomeDB = c_new1, ingredient = alc.ingredient, amount = alc.amount)
            newGene.save()
        for alc in c2_alcohol[alc_crossover:]: #add the second half of the alcohol from gene 2 to new gene 1
            if Gene.objects.filter(chromosomeDB = c_new1, ingredient = alc.ingredient).exists(): #check if we are about to add a duplicate ingredient
                index = random.randint(0, len(all_alcohol) - 1)
                rand_alc = all_alcohol[index]
                newGene = Gene(chromosomeDB = c_new1, ingredient = rand_alc, amount = amounts[random.randint(0,4)])
                newGene.save()
            else:
                newGene = Gene(chromosomeDB = c_new1, ingredient = alc.ingredient, amount = alc.amount)
                newGene.save()
        for alc in c1_alcohol[alc_crossover:]: #add the second half of the alcohol from gene 1 to new gene 2
            newGene = Gene(chromosomeDB = c_new2, ingredient = alc.ingredient, amount = alc.amount)
            newGene.save()
        for alc in c2_alcohol[:alc_crossover]: #add the first half of the alcohol from gene 2 to new gene 2
            if Gene.objects.filter(chromosomeDB = c_new2, ingredient = alc.ingredient).exists(): #check if we are about to add a duplicate ingredient
                index = random.randint(0, len(all_alcohol) - 1)
                rand_alc = all_alcohol[index]
                newGene = Gene(chromosomeDB = c_new2, ingredient = rand_alc, amount = amounts[random.randint(0,4)])
                newGene.save()
            else:
                newGene = Gene(chromosomeDB = c_new2, ingredient = alc.ingredient, amount = alc.amount)
                newGene.save()

        
        c1_mixer= Gene.objects.filter(chromosomeDB = c1, ingredient__type__contains = 'mixer')
        c2_mixer = Gene.objects.filter(chromosomeDB = c2, ingredient__type__contains = 'mixer')
        mix_crossover = random.randint(0, min(len(c1_mixer),len(c2_mixer)))
        for mix in c1_mixer[:mix_crossover]: #add the first half of the mixer from gene 1 to new gene 1
            newGene = Gene(chromosomeDB = c_new1, ingredient = mix.ingredient, amount = mix.amount)
            newGene.save()
        for mix in c2_mixer[mix_crossover:]: #add the second half of the mixer from gene 2 to new gene 1
            if Gene.objects.filter(chromosomeDB = c_new1, ingredient = mix.ingredient).exists(): #check if we are about to add a duplicate ingredient
                index = random.randint(0, len(all_mixers) - 1)
                rand_mix = all_mixers[index]
                newGene = Gene(chromosomeDB = c_new1, ingredient = rand_mix, amount = amounts[random.randint(0,6)])
                newGene.save()
            else:
                newGene = Gene(chromosomeDB = c_new1, ingredient = mix.ingredient, amount = mix.amount)
                newGene.save()
        for mix in c1_mixer[mix_crossover:]: #add the second half of the mixer from gene 1 to new gene 2
            newGene = Gene(chromosomeDB = c_new2, ingredient = mix.ingredient, amount = mix.amount)
            newGene.save()
        for mix in c2_mixer[:mix_crossover]: #add the first half of the mixer from gene 2 to new gene 2
            if Gene.objects.filter(chromosomeDB = c_new2, ingredient = mix.ingredient).exists(): #check if we are about to add a duplicate ingredient
                index = random.randint(0, len(all_mixers) - 1)
                rand_mix = all_mixers[index]
                newGene = Gene(chromosomeDB = c_new2, ingredient = rand_mix, amount = amounts[random.randint(0,6)])
                newGene.save()
            else:
                newGene = Gene(chromosomeDB = c_new2, ingredient = mix.ingredient, amount = mix.amount)
                newGene.save()
        
        c1_mod= Gene.objects.filter(chromosomeDB = c1, ingredient__type__contains = 'modifier')
        c2_mod = Gene.objects.filter(chromosomeDB = c2, ingredient__type__contains = 'modifier')
        mod_crossover = random.randint(0, min(len(c1_mod),len(c2_mod)))
        for mod in c1_mod[:mod_crossover]: #add the first half of the modifier from gene 1 to new gene 1
            newGene = Gene(chromosomeDB = c_new1, ingredient = mod.ingredient, amount = mod.amount)
            newGene.save()
        for mod in c2_mod[mod_crossover:]: #add the second half of the modifier from gene 2 to new gene 1
            if Gene.objects.filter(chromosomeDB = c_new1, ingredient = mod.ingredient).exists(): #check if we are about to add a duplicate ingredient
                index = random.randint(0, len(all_modifiers) - 1)
                rand_mod = all_modifiers[index]
                newGene = Gene(chromosomeDB = c_new1, ingredient = rand_mod, amount = amounts[random.randint(0,1)])
                newGene.save()
            else:
                newGene = Gene(chromosomeDB = c_new1, ingredient = mod.ingredient, amount = mod.amount)
                newGene.save()
        for mod in c1_mod[mod_crossover:]: #add the second half of the modifier from gene 1 to new gene 2
            newGene = Gene(chromosomeDB = c_new2, ingredient = mod.ingredient, amount = mod.amount)
            newGene.save()
        for mod in c2_mod[:mod_crossover]: #add the first half of the modifier from gene 2 to new gene 2
            if Gene.objects.filter(chromosomeDB = c_new2, ingredient = mod.ingredient).exists(): #check if we are about to add a duplicate ingredient
                index = random.randint(0, len(all_modifiers) - 1)
                rand_mod = all_modifiers[index]
                newGene = Gene(chromosomeDB = c_new2, ingredient = rand_mod, amount = amounts[random.randint(0,1)])
                newGene.save()
            else:
                newGene = Gene(chromosomeDB = c_new2, ingredient = mod.ingredient, amount = mod.amount)
                newGene.save()

        c_new1.save()
        c_new2.save()

        return c_new1, c_new2 #return new genes we created

    def mutation(self, c, new_population):
        special = ''
        c_new = ChromosomeDB(name = special, population = new_population) #we will change the name down below
        c_new.save()
        
        new_amount0 = Measurements(amount_ounces = 0)
        new_amount0.save()
        new_amount1 = Measurements(amount_ounces = 1)
        new_amount1.save()
        new_amount2 = Measurements(amount_ounces = 2)
        new_amount2.save()
        new_amount3 = Measurements(amount_ounces = 3)
        new_amount3.save()
        new_amount4 = Measurements(amount_ounces = 4)
        new_amount4.save()
        new_amount5 = Measurements(amount_ounces = 5)
        new_amount5.save()
        new_amount6= Measurements(amount_ounces = 6)
        new_amount6.save()
        amounts = [new_amount0, new_amount1, new_amount2, new_amount3, new_amount4, new_amount4, new_amount6]

        c_genes = Gene.objects.filter(chromosomeDB = c)
        num_points = random.randint(0, len(c_genes))
        subset = random.sample(range(0, len(c_genes)), num_points) #subset of random points
        
        all_alcohol = Ingredients.objects.filter(type = 'alcohol')
        all_mixers = Ingredients.objects.filter(type = 'mixer')
        all_modifiers = Ingredients.objects.filter(type = 'modifier')

        for i in range(0, len(c_genes)):
            if i in subset:
                gene_type = c_genes[i].ingredient.type
                if gene_type == 'alcohol':
                    index = random.randint(0, len(all_alcohol) - 1)
                    rand_alc = all_alcohol[index] #select new alcohol from all alcohol not just same category maybe want to change that?
                    new_gene = Gene(chromosomeDB = c_new, ingredient = rand_alc, amount = amounts[random.randint(0,4)]) 
                    new_gene.save()
                    special += str(new_gene.ingredient.name) + ' '
                elif gene_type == 'mixer':
                    index = random.randint(0, len(all_mixers) - 1)
                    rand_mix = all_mixers[index]
                    new_gene = Gene(chromosomeDB = c_new, ingredient = rand_mix, amount = amounts[random.randint(0,6)]) 
                    new_gene.save()
                    special += str(new_gene.ingredient.name) + ' '
                else:
                    index = random.randint(0, len(all_modifiers) - 1)
                    rand_mod = all_modifiers[index]
                    new_gene = Gene(chromosomeDB = c_new, ingredient = rand_mod, amount = amounts[random.randint(0,1)])
                    new_gene.save()
                    special += str(new_gene.ingredient.name) + ' '

        
        words1 = special.split()
        words2 = c.name.split()
        flip = random.randint(0,1)
        c_new_name = ""
        if flip == 0:
            combo = words1[0:int(len(words1)/2)] + words2[int(len(words2)/2):]
            for n in combo:
                c_new_name += n
                c_new_name += " "
        else:
            combo = words2[0:int(len(words2)/2)] + words1[int(len(words1)/2):]
            for n in combo:
                c_new_name += n
                c_new_name += " "
        c_new.name = c_new_name
        c_new.save()
        return c_new
    
    def gen_alg(self):
        n = 0
        while n < 3:
            print('n: ' + str(n))
            new_population = Population(user = self.user)
            new_population.save()
            cur_population = ChromosomeDB.objects.filter(population = self.training_population)
            pop_split = random.randint(0,len(cur_population))
            #print(pop_split)
            for chrom in range(0, pop_split, 2):
                self.crossover(cur_population[chrom], cur_population[chrom + 1], new_population)
            for chrom in range(pop_split, len(cur_population)):
                self.mutation(cur_population[chrom], new_population)
            new_input = self.get_new_train_input(new_population)
            omg = 0 #not sure what this is for
            for i in new_input:
                self.train_output.append(self.predictor.predict(X=[i])[0])
                omg += 1

            #add all of the chromosomes from the training set to the new_population we just created
            new_population_chromosomes = ChromosomeDB.objects.filter(population = new_population)
            for chrom in new_population_chromosomes:
                genes = Gene.objects.filter(chromosomeDB = chrom)
                new_chromosome = ChromosomeDB(name = chrom.name, population = self.training_population)
                new_chromosome.save()
                for gene in genes:
                    new_gene = Gene(chromosomeDB = new_chromosome, ingredient = gene.ingredient, amount = gene.amount)
                    new_gene.save()

            
            combined_population_chromosomes = ChromosomeDB.objects.filter(population = self.training_population)
            self.train_input += new_input #add new input data to our previous training input data
            data = list(zip(self.train_output, self.train_input, combined_population_chromosomes)) #creates tuples to link the the combined drink data, ratings, and combined drink objects
            data = sorted(data, key=lambda x: x[0],reverse=True) #sort the combined drink population by best rating
            next_generation = Population(user = self.user)
            next_generation.save()
            train_in = []
            train_out = []
            for d in range(min(len(data), 100)):
                old_chromosome = data[d][2]
                genes = Gene.objects.filter(chromosomeDB = old_chromosome)
                new_chromosome = ChromosomeDB(name = old_chromosome.name, population = next_generation, rating = data[d][0]) #could also take the rating from the old chromosome, should be the same
                new_chromosome.save()
                for gene in genes:
                    new_gene = Gene(chromosomeDB = new_chromosome, ingredient = gene.ingredient, amount = gene.amount)
                    new_gene.save()
                train_in.append(data[d][1])
                train_out.append(data[d][0])
            self.training_population = next_generation
            self.train_input = train_in
            self.train_output = train_out
            n += 1

    def create_fitness_func(self):
        self.predictor.fit(X=self.train_input, y=self.train_output)
        #test = [[0,2,0,0,0,0,10,0,0,0,0,0,0,0,0,0.5,0,0,0,0,1]]
        #outcome = self.predictor.predict(X=test)
        #coefficients = self.predictor.coef_
        #print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))
    def filter_drinks():
        diff = 0
        good_drinks = {}
        user_ingredients = AvailableIngredients.objects.filter(user = request.user)
        output_chromosomes = ChromosomeDB.objects.filter(population = gen_alg.training_population)
        for drink in output_chromosomes:
            genes = Gene.objects.filter(chromosomeDB = drink)
            for gene in genes:
                if gene.ingredient not in user_ingredients.ingredient:
                    diff += 1
            if diff not in good_drinks:
                good_drinks[diff] = []
            good_drinks[diff] = drink
        sorted_drinks = sorted(good_drinks.items())
        return sorted_drinks[0][1]
        
# def main(user):
#     gen_alg = GeneticAlgorithm(user)
#     gen_alg.create_fitness_func()
#     gen_alg.gen_alg()
#     output_chromosomes = ChromosomeDB.objects.filter(population = gen_alg.training_population)
#     for i in range(25):#range(len(gen_alg.population)):
#         chromosome = output_chromosomes[i]
#         genes = Gene.objects.filter(chromosomeDB = chromosome)
#         print(chromosome.name)
#         for gene in genes:
#             print(gene)
#         print(gen_alg.train_output[i])
#         print('\n')

# if __name__ == "__main__":
#     main()