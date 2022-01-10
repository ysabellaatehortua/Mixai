from sklearn.linear_model import LinearRegression
from random import random
from chromosome import Chromosome

class GeneticAlgorithm():

    def __init__(self, n = 0):
        self.population = []
        self.n = n
        self.train_input = list()
        self.train_output = list()
        self.ingredient_details = {}
    
    def population_setup(self):
        f = open("Database/Mixai/allRecipes.txt", "r")
        d = open("Database/Mixai/allDrinks.txt", "r")
        i = open("Database/Mixai/allIngredients.txt", "r")
        recipes = {}
        drinks = [] #store list of drinks
        ds = d.readlines() #read list of drinks 
        for drink in ds:
            drink = drink.rstrip()
            if drink != 'False':
                drinks.append(drink) #add each drink to list of drinks 
        #print(drinks)
        ingredients = {}
        ings = i.readlines()
        for ingredient in ings:
            ingredient = ingredient.rstrip().rsplit(' ', 1)
            ingredients[ingredient[0][0:len(ingredient[0]) - 1]] = ingredient[1]
            if ingredient[1] not in self.ingredient_details:
                self.ingredient_details[ingredient[1]] = []
            self.ingredient_details[ingredient[1]].append(ingredient[0][0:len(ingredient[0]) - 1])
        #print(ingredients)
        line = f.readline().rstrip()
        while line != '':
            drink = line.rstrip()
            #print(drink)
            if drink in drinks:
                chrom = Chromosome()
                line = f.readline()
                while line != '\n':
                    line = line.rstrip().split()
                    ingredient, index = self.ingredient_parser(line, ingredients)
                    amt = float(line[index])
                    #og_amt = float(line[index + 2])
                    #og_unit = line[index + 3]
                    if drink not in recipes:
                        recipes[drink] = []
                    recipes[drink].append([ingredient, amt]) #(og_unit, og_amt)])
                    chrom.name = drink
                    if ingredients[ingredient] == 'alcohol':
                        chrom.alcohol_types.append(ingredient)
                        chrom.alcohol_amts.append(amt)
                    if ingredients[ingredient] == 'liqueur':
                        chrom.liqueur_types.append(ingredient)
                        chrom.liqueur_amts.append(amt)
                    if ingredients[ingredient] == 'mixer':
                        chrom.mixer_types.append(ingredient)
                        chrom.mixer_amts.append(amt)
                    if ingredients[ingredient] == 'modifier':
                        chrom.modifier_types.append(ingredient)
                        chrom.modifier_amts.append(amt)
                    line = f.readline()
                    if line == '\n':
                        self.population.append(chrom)
                line = f.readline()
                line = f.readline().rstrip()
                #print(line)

    def ingredient_parser(self, ingredient, ingredients):
        four_word = ''
        four_word += ingredient[0]
        four_word += ' '
        four_word += ingredient[1]
        four_word += ' '
        four_word += ingredient[2]
        four_word += ' '
        four_word += ingredient[3]
        #print(four_word)
        if four_word in ingredients:
            return four_word, 4
        else: 
            three_word = ''
            three_word += ingredient[0]
            three_word += ' '
            three_word += ingredient[1]
            three_word += ' '
            three_word += ingredient[2]
            #print(three_word)
            if three_word in ingredients:
                return three_word, 3
            else:
                two_word = ''
                two_word += ingredient[0]
                two_word += ' '
                two_word += ingredient[1]
                #print(two_word)
                if two_word in ingredients:
                    return two_word, 2
                else:
                    #print(ingredient[0])
                    if ingredient[0] in ingredients:
                        return ingredient[0], 1
    
    def ingredient_deets(self):
        self.ingredient_details['alcohol'] = {'dark rum': 3, 'light rum': 3, 'vodka': 1, 'gin': 1, 'tequila': 1, 'peach vodka': 2, 'vanilla vodka': 2, 'absolut citron': 2, 'absolut vodka': 1, 'applejack': 4, 'vermouth': 0.5, 'scotch': 0.5, 'sweet vermouth': 0.5, 'dry vermouth': 0.5, 'blended whiskey': 0.5, 'bourbon': -0.5, 'blackberry brandy': 4, 'champagne': 0.1, 'rye whiskey': 0.5, 'rum': 3, '151 proof rum': 0.25, 'sloe gin': 1, 'cherry brandy': 4, 'spiced rum': 3, 'port': 4, 'brandy': 4, 'lillet blanc': 0.5, 'pisco': 0.5, 'dubonnet rouge': 0.5, 'absinthe': 0.25, 'apricot brandy': 4, 'cachaca': 3, 'mezcal': 1, 'cognac': 0.5, 'malibu rum': 2, 'white rum': 3, 'whiskey': 0.5, 'irish whiskey': 0.5, 'peach brandy': 4, 'jack daniels': 0.5, 'apple brandy': 4, 'cranberry vodka': 2, 'beer': .1, 'southern comfort': 2, 'blended scotch': 0.5, 'islay single malt scotch': 0.5, 'everclear': 0.25, 'prosecco': 1, 'coffee brandy': 4, 'lime vodka': 2, 'red wine': 0.1, 'ricard': 0.5, 'ruby port': 4, 'anis': 0.25, 'rosso vermouth': 0.5, 'gold rum': 3, 'pernod': 0.25, 'jägermeister': 3, 'zima': 0.1}
        self.ingredient_details['mixer'] = {'sweet': ['orange juice', 'coca-cola', 'cranberry juice',  'tonic water', 'grapefruit juice', 'peach nectar', 'pineapple juice', 'passion fruit juice', 'hot chocolate',  'ginger ale', 'ginger beer',  'pomegranate juice',  'lemonade', 'iced tea', 'schweppes russchian', 'apple juice',  'grape soda', 'coconut milk', '7-up', 'root beer', 'coca cola', 'cream soda'], 'nonsweet': ['milk', 'tomato juice', 'coffee'], 'neutral': ['carbonated water', 'water', 'soda water']}
        self.ingredient_details['modifier'] = {'sweet':['roses sweetened lime juice', 'sugar', 'sugar syrup', 'demerara sugar', 'pineapple syrup', 'vanilla syrup', 'rose', 'strawberries', 'honey', 'apricot nectar', 'powdered sugar',  'maraschino cherry', 'aperol', 'orgeat syrup',  'honey syrup',  'pineapple', 'passion fruit syrup',  'raspberry syrup', 'blood orange',  'maple syrup'],'neutral': ['heavy cream', 'light cream', 'espresso', 'egg', 'sweet and sour', 'ginger syrup', 'allspice', 'salt'],'sour': ['lemon juice', 'lime juice', 'sour mix', 'fresh lime juice', 'lime']}

    def train_input_setup(self):
        drinks = []
        for drink in self.population:
            total_alc = 0
            for alc in range(len(drink.alcohol_amts)):
                total_alc += alc * self.ingredient_details['alcohol'][drink.alcohol_types[alc]]
            total_liq = 0
            for liq in range(len(drink.liqueur_amts)):
                total_liq += drink.liqueur_amts[liq]
            total_mix = 0
            for mix in range(len(drink.mixer_amts)):
                if drink.mixer_types[mix] in self.ingredient_details['mixer']['sweet']:
                    total_mix += drink.mixer_amts[mix]*0.8
                else:
                    total_mix += drink.mixer_amts[mix]
            total_mod = 0
            for mod in range(len(drink.modifier_amts)):
                if drink.modifier_types[mod] in self.ingredient_details['modifier']['sour']:
                    total_mod += drink.modifier_amts[mod]*0.5
                else:  
                    total_mod += drink.modifier_amts[mod]
            d = [total_alc, total_liq, total_mix, total_mod]
            self.train_input.append(d)
            #drinks.append(drink.name)
            #self.train_output.append(10)
        self.train_output = [3, 5, 7, 9, 10, 7, 4, 6, 4, 7, 7, 3, 4, 10, 8, 1, 2, 2, 3, 8, 6, 7, 9, 10, 3, 9, 5, 10, 3, 9, 3, 3, 2, 1, 4, 4, 3, 10, 8, 6, 7, 5, 9, 6, 10, 10, 3, 4, 3, 10, 4, 4, 7, 10, 10, 7, 7, 3, 1, 7, 10, 3, 10, 10, 10, 10, 4, 6, 6, 6, 7, 10, 10, 1, 8, 9, 9, 7, 5, 7, 4, 10, 6, 10, 10, 4, 4, 3, 3, 3, 5, 5, 4, 6, 6, 3, 6, 7, 7, 9, 8, 8, 7, 7, 4]
        #return drinks
    
    #def make_bad_drinks(self):

    def crossover(self, c1, c2):
        crossover = random.randint(0, 11) #generate random crossover point p 0,...,n
        portion = crossover / 10
        c_new1 = chromosome()
        c_new2 = chromosome()

        alc_crossover = int(portion*len(c1.alcohol_types))
        c_new1.alcohol_types = c1.alcohol_types[:alc_crossover] + c2.alcohol_types[alc_crossover:]
        c_new2.alcohol_types = c2.alcohol_types[:alc_crossover] + c1.alcohol_types[alc_crossover:]
        
        liq_crossover = int(portion*len(c1.liqueur_types))
        c_new1.liqueur_types = c1.liqueur_types[:liq_crossover] + c2.liqueur_types[liq_crossover:]
        c_new2.liqueur_types = c2.liqueur_types[:liq_crossover] + c1.liqueur_types[liq_crossover:]
        
        mix_crossover = int(portion*len(c1.mixer_types))
        c_new1.mixer_types = c1.mixer_types[:mix_crossover] + c2.mixer_types[mix_crossover:]
        c_new2.mixer_types = c2.mixer_types[:mix_crossover] + c1.mixer_types[mix_crossover:]
        
        mod_crossover = int(portion*len(c1.modifier_types))
        c_new1.modifier_types = c1.modifier_types[:mod_crossover] + c2.modifier_types[mod_crossover:]
        c_new2.modifier_types = c2.modifier_types[:mod_crossover] + c1.modifier_types[mod_crossover:]
        
        return c_new1, c_new2

    def mutation(self, c):
        num_points = random.randint(0, 4) #size of subset of random points
        subset = random.sample(range(0, 4), num_points) #subset of random points
        c_new = chromosome()
        for i in range(0, n):
            if i in subset:
                c_new.attributes[i] = random.randint(0, 11) #how to randomize drink type
            else:
                c_new.attributes[i] = c.attributes[i]
        c_new.set_from_attributes()
        return c_new
    
    def gen_alg(self):
        n = 0
        while n < 100:
            crossover(population)
    
    def create_fitness_func(self):
        predictor = LinearRegression(n_jobs=-1)
        predictor.fit(X=self.train_input, y=self.train_output)
        test = [[3, 0, 12, 0]]
        outcome = predictor.predict(X=test)
        coefficients = predictor.coef_
        print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))
    
def main():
    gen_alg = GeneticAlgorithm()
    gen_alg.population_setup()
    #print(gen_alg.population)
    #print(gen_alg.ingredient_details)
    gen_alg.ingredient_deets()
    #print(gen_alg.ingredient_details)
    gen_alg.train_input_setup()
    #print('\n')
    #print(gen_alg.train_input)
    gen_alg.create_fitness_func()

if __name__ == "__main__":
    main()