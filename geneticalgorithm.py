from sklearn.linear_model import LinearRegression
import random
import copy 
from chromosome import Chromosome

class GeneticAlgorithm():

    def __init__(self, n = 0):
        self.population = []
        self.n = n
        self.train_input = list()
        self.train_output = list()
        self.ingredient_list = {}
        self.simple_types = {}
        self.predictor = LinearRegression(n_jobs=-1)
    
    def population_setup(self):
        f = open("convertedTrainingRecipes.txt", "r")
        i = open("normalIngredients.txt", "r")
        recipes = {}
        ingredients = {}
        ingredients['Alcohol'] = {}
        ingredients['Mixer'] = {}
        ingredients['Modifier'] = {}
        self.simple_types['Alcohol'] = []
        self.simple_types['Mixer'] = []
        self.simple_types['Modifier'] = []
        ings = i.readlines()
        for ingredient in ings:
            ingredient = ingredient.rstrip().rsplit('  ')
            if ingredient[2][10:] == 'Yes':
                if ingredient[1][6:] not in ingredients['Alcohol']:
                    ingredients['Alcohol'][ingredient[1][6:]] = []
                ingredients['Alcohol'][ingredient[1][6:]].append(ingredient[0])
                self.ingredient_list[ingredient[0]] = ('Alcohol', ingredient[1][6:])
                self.simple_types['Alcohol'].append(ingredient[0])
            else:
                if ingredient[1][6:11] == 'Mixer':
                    if ingredient[1][12:] not in ingredients['Mixer']:
                        ingredients['Mixer'][ingredient[1][12:]] = []
                    ingredients['Mixer'][ingredient[1][12:]].append(ingredient[0])
                    self.ingredient_list[ingredient[0]] = ('Mixer', ingredient[1][12:])
                    self.simple_types['Mixer'].append(ingredient[0])
                if ingredient[1][6:14] == 'Modifier':
                    if ingredient[1][15:] not in ingredients['Modifier']:
                        ingredients['Modifier'][ingredient[1][15:]] = []
                    ingredients['Modifier'][ingredient[1][15:]].append(ingredient[0])
                    self.ingredient_list[ingredient[0]] = ('Modifier', ingredient[1][15:])
                    self.simple_types['Modifier'].append(ingredient[0])
        print(self.simple_types)

        line = f.readline().rstrip()
        while line != '':
            drink = line
            chrom = Chromosome()
            line = f.readline()
            while line != '\n' and line != '':
                line = line.rstrip().split('  ')
                ingredient = line[0]
                special = ['Spice', 'Ice', 'Garnish', 'Fruit', 'Unique']
                if self.ingredient_list[ingredient][1] not in special:
                    amt = float(line[1])
                og_amt = line[2]
                chrom.name = drink
                info = self.ingredient_list[ingredient]
                kind = info[0]
                if kind == 'Alcohol':
                    chrom.alcohol_types.append(ingredient)
                    chrom.alcohol_amts.append(amt)
                if kind == 'Mixer':
                    chrom.mixer_types.append(ingredient)
                    chrom.mixer_amts.append(amt)
                if kind == 'Modifier':
                    chrom.modifier_types.append(ingredient)
                    chrom.modifier_amts.append(amt)
                line = f.readline()
                if line == '\n' or line == '':
                    self.population.append(chrom)
            line = f.readline().rstrip()
            #line = f.readline()
            #print(line)

    def train_input_setup(self, population):
        drinks = []
        train_input = []
        for drink in population:
            total_alc = [0, 0, 0, 0, 0, 0]
            for alc in range(len(drink.alcohol_amts)):
                a, d_type = self.ingredient_list[drink.alcohol_types[alc]]
                if d_type == 'Rum':
                    total_alc[0] += drink.alcohol_amts[alc]
                if d_type == 'Spirit':
                    total_alc[1] += drink.alcohol_amts[alc]
                if d_type == 'Whiskey':
                    total_alc[2] += drink.alcohol_amts[alc]
                if d_type == 'Liqueur':
                    total_alc[3] += drink.alcohol_amts[alc]
                if d_type == 'Beer':
                    total_alc[4] += drink.alcohol_amts[alc]
                if d_type == 'Wine':
                    total_alc[5] += drink.alcohol_amts[alc]
            total_mix = [0,0,0,0,0,0,0]
            for mix in range(len(drink.mixer_amts)):
                m, m_type = self.ingredient_list[drink.mixer_types[mix]]
                if m_type == 'Juice':
                    total_mix[0] += drink.mixer_amts[mix]
                if m_type == 'Dairy':
                    total_mix[1] += drink.mixer_amts[mix]
                if m_type == 'Soda':
                    total_mix[2] += drink.mixer_amts[mix]
                if m_type == 'Coffee':
                    total_mix[3] += drink.mixer_amts[mix]
                if m_type == 'Mix':
                    total_mix[4] += drink.mixer_amts[mix]
                if m_type == 'Water':
                    total_mix[5] += drink.mixer_amts[mix]
                if m_type == 'Unique':
                    total_mix[6] += drink.mixer_amts[mix]
            total_mod = [0,0,0,0,0,0,0,0]
            for mod in range(len(drink.modifier_amts)):
                m, m_type = self.ingredient_list[drink.modifier_types[mod]]
                if m_type == 'Bitter':
                    total_mod[0] += drink.modifier_amts[mod]
                if m_type == 'Fruit':
                    total_mod[1] += drink.modifier_amts[mod]
                if m_type == 'Sweetner':
                    total_mod[2] += drink.modifier_amts[mod]
                if m_type == 'Garnish':
                    total_mod[3] += drink.modifier_amts[mod]
                if m_type == 'Ice':
                    total_mod[4] += drink.modifier_amts[mod]
                if m_type == 'Sauce':
                    total_mod[5] += drink.modifier_amts[mod]
                if m_type == 'Spice':
                    total_mod[6] += drink.modifier_amts[mod]
                if m_type == 'Sour':
                    total_mod[7] += drink.modifier_amts[mod]
            d = total_alc + total_mix + total_mod
            train_input.append(d)
        return train_input

    def make_initial_io(self):
        self.train_input = self.train_input_setup(self.population)
        o = open("train_out.txt", "r")
        lines = o.readlines()
        for l in lines:
            self.train_output.append(int(l.strip()))
        
    def crossover(self, c1, c2):
        c_new1 = Chromosome()
        c_new2 = Chromosome()

        words1 = c1.name.split()
        words2 = c2.name.split()
        combo1 = words1[0:int(len(words1)/2)] + words2[int(len(words2)/2):]
        for n in combo1:
            c_new1.name += n
            c_new1.name += " "
        combo2 = words2[0:int(len(words2)/2)] + words1[int(len(words1)/2):]
        for n in combo2:
            c_new2.name += n
            c_new2.name += " "
        
        alc_crossover = random.randint(0, min(len(c1.alcohol_types),len(c2.alcohol_types)))
        c_new1.alcohol_types = c1.alcohol_types[:alc_crossover] + c2.alcohol_types[alc_crossover:]
        c_new1.alcohol_amts = c1.alcohol_amts[:alc_crossover] + c2.alcohol_amts[alc_crossover:]
        c_new2.alcohol_types = c2.alcohol_types[:alc_crossover] + c1.alcohol_types[alc_crossover:]
        c_new2.alcohol_amts = c2.alcohol_amts[:alc_crossover] + c1.alcohol_amts[alc_crossover:]
        
        mix_crossover = random.randint(0, min(len(c1.mixer_types), len(c2.mixer_types)))
        c_new1.mixer_types = c1.mixer_types[:mix_crossover] + c2.mixer_types[mix_crossover:]
        c_new1.mixer_amts = c1.mixer_amts[:mix_crossover] + c2.mixer_amts[mix_crossover:]
        c_new2.mixer_types = c2.mixer_types[:mix_crossover] + c1.mixer_types[mix_crossover:]
        c_new2.mixer_amts = c2.mixer_amts[:mix_crossover] + c1.mixer_amts[mix_crossover:]
        
        mod_crossover = random.randint(0, min(len(c1.modifier_types), len(c2.modifier_types)))
        c_new1.modifier_types = c1.modifier_types[:mod_crossover] + c2.modifier_types[mod_crossover:]
        c_new1.modifier_amts = c1.modifier_amts[:mod_crossover] + c2.modifier_amts[mod_crossover:]
        c_new2.modifier_types = c2.modifier_types[:mod_crossover] + c1.modifier_types[mod_crossover:]
        c_new2.modifier_amts = c2.modifier_amts[:mod_crossover] + c1.modifier_amts[mod_crossover:]
        
        return c_new1, c_new2

    def mutation(self, c):
        c_new = Chromosome()
        special = ''
        alc_num_points = random.randint(0, len(c.alcohol_types)) #size of subset of random points
        alc_subset = random.sample(range(0, len(c.alcohol_types)), alc_num_points) #subset of random points
        c_new.alcohol_types = c.alcohol_types
        c_new.alcohol_amts = c.alcohol_amts
        for i in range(0, len(c.alcohol_types)):
            if i in alc_subset:
                new_alc = random.randint(0,len(self.simple_types['Alcohol']) - 1)
                c_new.alcohol_types[i] = self.simple_types['Alcohol'][new_alc]
                c_new.alcohol_amts[i] = random.randint(1,4)
                special += c_new.alcohol_types[i] + ' '
        
        mix_num_points = random.randint(0, len(c.mixer_types)) #size of subset of random points
        mix_subset = random.sample(range(0, len(c.mixer_types)), mix_num_points) #subset of random points
        c_new.mixer_types = c.mixer_types
        c_new.mixer_amts = c.mixer_amts
        for i in range(0, len(c.mixer_types)):
            if i in mix_subset:
                new_mix = random.randint(0,len(self.simple_types['Mixer']) - 1)
                c_new.mixer_types[i] = self.simple_types['Mixer'][new_mix]
                c_new.mixer_amts[i] = random.randint(1,6)
                special += c_new.mixer_types[i] + ' '
        
        mod_num_points = random.randint(0, len(c.modifier_types)) #size of subset of random points
        mod_subset = random.sample(range(0, len(c.modifier_types)), mod_num_points) #subset of random points
        c_new.modifier_types = c.modifier_types
        c_new.modifier_amts = c.modifier_amts
        for i in range(0, len(c.modifier_types)):
            if i in mod_subset:
                new_mod = random.randint(0,len(self.simple_types['Modifier']) - 1)
                c_new.modifier_types[i] = self.simple_types['Modifier'][new_mod]
                c_new.modifier_amts[i] = random.randint(1,2)
                special += c_new.modifier_types[i]
        
        words1 = special.split()
        words2 = c.name.split()
        flip = random.randint(0,1)
        if flip == 0:
            combo = words1[0:int(len(words1)/2)] + words2[int(len(words2)/2):]
            for n in combo:
                c_new.name += n
                c_new.name += " "
        else:
            combo = words2[0:int(len(words2)/2)] + words1[int(len(words1)/2):]
            for n in combo:
                c_new.name += n
                c_new.name += " "
        return c_new
    
    def gen_alg(self):
        n = 0
        avg = []
        avg.append(sum(self.train_output) / len(self.train_output))
        distribution = []
        distribution.append(self.train_output)
        while n < 25:
            new_population = []
            pop_split = random.randint(0,len(self.population))
            #print(pop_split)
            for chrom in range(0, pop_split, 2):
                c1, c2 = self.crossover(self.population[chrom], self.population[chrom + 1])
                new_population.append(c1)
                new_population.append(c2)
            for chrom in range(pop_split, len(self.population)):
                c = self.mutation(self.population[chrom])
                new_population.append(c)
            new_input = self.train_input_setup(new_population)
            omg = 0
            for i in new_input:
                self.train_output.append(self.predictor.predict(X=[i])[0])
                omg += 1
            self.population += new_population
            self.train_input += new_input
            data = list(zip(self.train_output, self.train_input, self.population))
            data = sorted(data, key=lambda x: x[0],reverse=True)
            pop = []
            train_in = []
            train_out = []
            for d in range(min(len(data), 100)):
                pop.append(data[d][2])
                train_in.append(data[d][1])
                train_out.append(data[d][0])
            self.population = pop
            self.train_input = train_in
            self.train_output = train_out
            n += 1
            avg.append(sum(self.train_output) / len(self.train_output))
            distribution.append(self.train_output)
        return avg, distribution

    def create_fitness_func(self):
        self.predictor.fit(X=self.train_input, y=self.train_output)

    def parse_ingredients(self, users_list):
        user_good = {}
        for drink in self.population:
            diff = 0
            for a in drink.alcohol_types:
                if a not in users_list:
                    diff += 1
            for mod in drink.modifier_types:
                if mod not in users_list:
                    diff += 1
            for mix in drink.mixer_types:
                if mix not in users_list:
                    diff += 1
            if diff not in user_good:
                user_good[diff] = []
            user_good[diff].append(drink)
        for d in user_good:
            print(d + len(user_good[d]))
        return user_good
    
def main():
    gen_alg = GeneticAlgorithm()
    gen_alg.population_setup()
    gen_alg.make_initial_io()
    gen_alg.create_fitness_func()
    avg, distrib = gen_alg.gen_alg()

if __name__ == "__main__":
    main()