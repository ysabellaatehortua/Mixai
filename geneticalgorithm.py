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
        f = open("trainingSetRecipes.txt", "r")
        #d = open("Database/Mixai/allDrinks.txt", "r")
        i = open("normalIngredients.txt", "r")
        recipes = {}
        #drinks = [] #store list of drinks
        #ds = d.readlines() #read list of drinks 
        #for drink in ds:
            #drink = drink.rstrip()
            #if drink != 'False':
                #drinks.append(drink) #add each drink to list of drinks 
        #print(drinks)
        ingredients = {}
        ingredients['Alcohol'] = {}
        ingredients['Mixer'] = {}
        ingredients['Modifier'] = {}
        ings = i.readlines()
        for ingredient in ings:
            ingredient = ingredient.rstrip().rsplit('  ')
            #print(ingredient)
            if ingredient[2][10:] == 'Yes':
                if ingredient[1][6:] not in ingredients['Alcohol']:
                    ingredients['Alcohol'][ingredient[1][6:]] = []
                ingredients['Alcohol'][ingredient[1][6:]].append(ingredient[0])
            else:
                #print("Mixer?: " + ingredient[1][6:12])
                if ingredient[1][6:11] == 'Mixer':
                    #print(ingredient[1][12:])
                    if ingredient[1][12:] not in ingredients['Mixer']:
                        ingredients['Mixer'][ingredient[1][12:]] = []
                    ingredients['Mixer'][ingredient[1][12:]].append(ingredient[0])
                #print("Mod?: " + ingredient[1][6:14])
                if ingredient[1][6:14] == 'Modifier':
                    #print(ingredient[1][15:])
                    if ingredient[1][15:] not in ingredients['Modifier']:
                        ingredients['Modifier'][ingredient[1][15:]] = []
                    ingredients['Modifier'][ingredient[1][15:]].append(ingredient[0])
            #ingredients[ingredient[0][0:len(ingredient[0]) - 1]] = ingredient[1]
            #if ingredient[1] not in self.ingredient_details:
                #self.ingredient_details[ingredient[1]] = []
            #self.ingredient_details[ingredient[1]].append(ingredient[0][0:len(ingredient[0]) - 1])
        #print(ingredients)
        line = f.readline().rstrip()
        while line != '':
            drink = line.rsplit(":")[0]
            print(drink)
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
                if ingredients['Alcohol'] == 'alcohol':
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
        #self.ingredient_details['alcohol'] = {'dark rum': 3, 'light rum': 3, 'vodka': 1, 'gin': 1, 'tequila': 1, 'peach vodka': 2, 'vanilla vodka': 2, 'absolut citron': 2, 'absolut vodka': 1, 'applejack': 4, 'vermouth': 0.5, 'scotch': 0.5, 'sweet vermouth': 0.5, 'dry vermouth': 0.5, 'blended whiskey': 0.5, 'bourbon': -0.5, 'blackberry brandy': 4, 'champagne': 0.1, 'rye whiskey': 0.5, 'rum': 3, '151 proof rum': 0.25, 'sloe gin': 1, 'cherry brandy': 4, 'spiced rum': 3, 'port': 4, 'brandy': 4, 'lillet blanc': 0.5, 'pisco': 0.5, 'dubonnet rouge': 0.5, 'absinthe': 0.25, 'apricot brandy': 4, 'cachaca': 3, 'mezcal': 1, 'cognac': 0.5, 'malibu rum': 2, 'white rum': 3, 'whiskey': 0.5, 'irish whiskey': 0.5, 'peach brandy': 4, 'jack daniels': 0.5, 'apple brandy': 4, 'cranberry vodka': 2, 'beer': .1, 'southern comfort': 2, 'blended scotch': 0.5, 'islay single malt scotch': 0.5, 'everclear': 0.25, 'prosecco': 1, 'coffee brandy': 4, 'lime vodka': 2, 'red wine': 0.1, 'ricard': 0.5, 'ruby port': 4, 'anis': 0.25, 'rosso vermouth': 0.5, 'gold rum': 3, 'pernod': 0.25, 'jägermeister': 3, 'zima': 0.1}
        #self.ingredient_details['mixer'] = {'sweet': ['orange juice', 'coca-cola', 'cranberry juice',  'tonic water', 'grapefruit juice', 'peach nectar', 'pineapple juice', 'passion fruit juice', 'hot chocolate',  'ginger ale', 'ginger beer',  'pomegranate juice',  'lemonade', 'iced tea', 'schweppes russchian', 'apple juice',  'grape soda', 'coconut milk', '7-up', 'root beer', 'coca cola', 'cream soda'], 'nonsweet': ['milk', 'tomato juice', 'coffee'], 'neutral': ['carbonated water', 'water', 'soda water']}
        #self.ingredient_details['modifier'] = {'sweet':['roses sweetened lime juice', 'sugar', 'sugar syrup', 'demerara sugar', 'pineapple syrup', 'vanilla syrup', 'rose', 'strawberries', 'honey', 'apricot nectar', 'powdered sugar',  'maraschino cherry', 'aperol', 'orgeat syrup',  'honey syrup',  'pineapple', 'passion fruit syrup',  'raspberry syrup', 'blood orange',  'maple syrup'],'neutral': ['heavy cream', 'light cream', 'espresso', 'egg', 'sweet and sour', 'ginger syrup', 'allspice', 'salt'],'sour': ['lemon juice', 'lime juice', 'sour mix', 'fresh lime juice', 'lime']}
        self.ingredient_details['alcohol'] = {}
        self.ingredient_details['alcohol']['dark'] = ['scotch', 'blended whiskey', 'bourbon', 'rye whiskey', 'blended scotch', 'islay single malt scotch', 'cognac', 'whiskey', 'irish whiskey', 'jack daniels']
        self.ingredient_details['alcohol']['clear'] = ['vodka', 'tequila', 'absolut vodka',  'mezcal']
        self.ingredient_details['alcohol']['sweet'] = ['gin', 'peach vodka', 'vanilla vodka', 'absolut citron', 'malibu rum', 'lime vodka', 'cranberry vodka', 'dark rum', 'light rum', 'white rum', 'rum', 'gold rum', 'spiced rum', 'cachaca', 'jägermeister']
        self.ingredient_details['alcohol']['bitter'] = ['red wine', 'vermouth', 'white wine', 'beer', 'champagne', 'prosecco', 'rose']
        
        self.ingredient_details['mixer'] = {}
        self.ingredient_details['mixer']['sweet'] = ['orange juice', 'coca-cola', 'tonic water', 'peach nectar', 'pineapple juice', 'ginger ale', 'ginger beer', 'apple juice',  'grape soda', '7-up', 'root beer', 'red gatorade', 'blue gatorade', 'yellow gatorade', 'orange gatorade', 'red bull', 'monster', 'rockstar', 'bang', 'cream soda']
        self.ingredient_details['mixer']['sour'] = ['passionfruit juice', 'pomegranate juice', 'lemonade']
        self.ingredient_details['mixer']['bitter'] = ['cranberry juice', 'grapefruit juice', 'iced tea', 'coffee']
        self.ingredient_details['mixer']['weird'] = ['hot chocolate', 'coconut milk', 'coffee', 'tomato juice']
        self.ingredient_details['mixer']['neutral'] = ['carbonated water', 'water', 'soda water']
        
        self.ingredient_details['modifier'] = {}
        self.ingredient_details['modifier']['sweet'] = ['sugar', 'sugar syrup', 'pineapple syrup', 'strawberries', 'honey', 'apricot nectar', 'powdered sugar',  'maraschino cherry',  'honey syrup',  'pineapple', 'passion fruit syrup',  'raspberry syrup', 'maple syrup', 'grenadine']
        self.ingredient_details['modifier']['sour'] = ['lemon juice', 'lime juice', 'sour mix', 'fresh lime juice', 'lime', 'blood orange']
        self.ingredient_details['modifier']['bitter'] = ['espresso']
        self.ingredient_details['modifier']['weird'] = ['heavy cream', 'light cream', 'allspice', 'rose', 'sweet and sour']
        self.ingredient_details['modifier']['neutral'] = ['egg', 'ginger syrup']
        self.ingredient_details['modifier']['salty']= ['salt']

        self.ingredient_details['liqueur'] = {}
        self.ingredient_details['liqueur']['sweet'] = ['peach schnapps', 'blue curacao', 'midori melon liqueur', 'melon liqueur', 'coconut liqueur',  'cherry liqueur', 'triple sec', 'elderflower cordial', 'cointreau', 'raspberry liqueur']
        self.ingredient_details['liqueur']['bitter'] = ['coffee liqueur', 'campari', 'passoa']
        self.ingredient_details['liqueur']['weird'] = ['kahlua', 'baileys irish cream', 'amaretto']

    def train_input_setup(self):
        drinks = []
        for drink in self.population:
            total_alc = [0, 0, 0, 0]
            for alc in range(len(drink.alcohol_amts)):
                if drink.alcohol_types[alc] in self.ingredient_details['alcohol']['dark']:
                    total_alc[0] += drink.alcohol_amts[alc]
                if drink.alcohol_types[alc] in self.ingredient_details['alcohol']['clear']:
                    total_alc[1] += drink.alcohol_amts[alc]
                if drink.alcohol_types[alc] in self.ingredient_details['alcohol']['sweet']:
                    total_alc[2] += drink.alcohol_amts[alc]
                if drink.alcohol_types[alc] in self.ingredient_details['alcohol']['bitter']:
                    total_alc[3] += drink.alcohol_amts[alc]
            total_liq = [0, 0, 0, 0]
            for liq in range(len(drink.liqueur_amts)):
                if drink.liqueur_types[liq] in self.ingredient_details['liqueur']['sweet']:
                    total_liq[0] += drink.liqueur_amts[liq] 
                if drink.liqueur_types[liq] in self.ingredient_details['liqueur']['bitter']:
                    total_liq[2] += drink.liqueur_amts[liq] 
                if drink.liqueur_types[liq] in self.ingredient_details['liqueur']['weird']:
                    total_liq[3] += drink.liqueur_amts[liq]
            total_mix = [0,0,0,0,0]
            for mix in range(len(drink.mixer_amts)):
                if drink.mixer_types[mix] in self.ingredient_details['mixer']['sweet']:
                    total_mix[0] += drink.mixer_amts[mix]
                if drink.mixer_types[mix] in self.ingredient_details['mixer']['sour']:
                    total_mix[1] += drink.mixer_amts[mix]
                if drink.mixer_types[mix] in self.ingredient_details['mixer']['bitter']:
                    total_mix[2] += drink.mixer_amts[mix]
                if drink.mixer_types[mix] in self.ingredient_details['mixer']['weird']:
                    total_mix[3] += drink.mixer_amts[mix]
                if drink.mixer_types[mix] in self.ingredient_details['mixer']['neutral']:
                    total_mix[4] += drink.mixer_amts[mix]
            total_mod = [0,0,0,0,0,0]
            for mod in range(len(drink.modifier_amts)):
                if drink.modifier_types[mod] in self.ingredient_details['modifier']['sweet']:
                    total_mod[0] += drink.modifier_amts[mod]
                if drink.modifier_types[mod] in self.ingredient_details['modifier']['sour']:
                    total_mod[1] += drink.modifier_amts[mod]
                if drink.modifier_types[mod] in self.ingredient_details['modifier']['bitter']:
                    total_mod[2] += drink.modifier_amts[mod]
                if drink.modifier_types[mod] in self.ingredient_details['modifier']['weird']:
                    total_mod[3] += drink.modifier_amts[mod]
                if drink.modifier_types[mod] in self.ingredient_details['modifier']['neutral']:
                    total_mod[4] += drink.modifier_amts[mod]
                if drink.modifier_types[mod] in self.ingredient_details['modifier']['salty']:
                    total_mod[5] += drink.modifier_amts[mod]
            d = total_alc + total_liq + total_mix + total_mod
            self.train_input.append(d)
            #drinks.append(drink.name)
            #self.train_output.append(10)
        self.train_output = [5, 10, 9, 5, 7, 9, 9, 7, 3, 10, 1, 1, 9, 8, 9, 10, 7, 7, 10, 9, 7, 8, 3, 9, 8, 8, 9, 9, 8, 8, 7, 9, 1, 7, 7, 10, 10, 8, 7, 2, 1, 10, 3, 10, 8, 8, 9, 3, 6, 4, 2, 8, 7, 7, 6, 7, 10, 2, 5, 10, 8, 7, 1]
        print(len(self.train_input))
        print(len(self.train_output))
    
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