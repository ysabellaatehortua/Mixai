from random import random
import chromosome

class GeneticAlgorithm():

    def __init__(self, population, n):
        self.population = population
        self.n = n
    
    def crossover(self, c1, c2):
        crossover = random.randint(0, n) #generate random crossover point p 0,...,n
        c_new1 = chromosome()
        c_new1.attributes = c1[:crossover] + c2[crossover:]
        c_new1.set_from_attributes()
        c_new2 = chromosome()
        c_new2.attributes = c2[:crossover] + c1[crossover:]
        c_new2.set_from_attributes()
        return c_new1, c_new2

    def mutation(self, c):
        num_points = random.randint(0, n) #size of subset of random points
        subset = random.sample(range(0, n), num_points) #subset of random points
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