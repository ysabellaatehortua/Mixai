class Chromosome():

    def __init__(self, name, alcohol_types, alcohol_amts, modifier_types, modifier_amts, mixer_types, mixer_amts):
        self.name = name
        self.alcohol_types = alcohol_types
        self.alcohol_amts = alcohol_amts
        #self.liqueur_types = liqueur_types
        #self.liqueur_amts = liqueur_amts
        self.modifier_types = modifier_types
        self.modifier_amts = modifier_amts
        self.mixer_types = mixer_types
        self.mixer_amts = mixer_amts
        #self.attributes = [alcohol_types, alcohol_amts, modifier_types, modifier_amts, mixer_types, mixer_amts]
        #self.attributes = [alcohol_types, alcohol_amts, liqueur_types, liqueur_amts, modifier_types, modifier_amts, mixer_types, mixer_amts]

    def __init__(self):
        self.name = ''
        self.alcohol_types = []
        self.alcohol_amts = []
        #self.liqueur_types = []
        #self.liqueur_amts = []
        self.modifier_types = []
        self.modifier_amts = []
        self.mixer_types = []
        self.mixer_amts = []
        #self.attributes = [self.alcohol_types, self.alcohol_amts, self.liqueur_types, self.liqueur_amts, self.modifier_types, self.modifier_amts, self.mixer_types, self.mixer_amts]
        #self.attributes = [self.alcohol_types, self.alcohol_amts, self.modifier_types, self.modifier_amts, self.mixer_types, self.mixer_amts]
    """
    def set_from_attributes(self):
        self.name = ''
        self.alcohol_types = self.attributes[0]
        self.alcohol_amts = self.attributes[1]
        #self.liqueur_types = self.attributes[2]
        #self.liqueur_amts = self.attributes[3]
        self.modifier_types = self.attributes[4]
        self.modifier_amts = self.attributes[5]
        self.mixer_types = self.attributes[6]
        self.mixer_amts = self.attributes[7]"""

    def __str__(self):
        chromosome = self.name
        chromosome += '\n'
        chromosome += str(self.alcohol_types)
        chromosome += str(self.alcohol_amts)
        #chromosome += str(self.liqueur_types)
        #chromosome += str(self.liqueur_amts)
        chromosome += str(self.modifier_types)
        chromosome += str(self.modifier_amts)
        chromosome += str(self.mixer_types)
        chromosome += str(self.mixer_amts)
        return chromosome
    
    def __repr__(self):
        chromosome = self.name
        chromosome += ' {\n'
        chromosome += 'alcohol_types: '
        chromosome += str(self.alcohol_types)
        chromosome += '\nalcohol_amts: '
        chromosome += str(self.alcohol_amts)
        #chromosome += '\nliqueur_types: '
        #chromosome += str(self.liqueur_types)
        #chromosome += '\nliqueur_amts: '
        #chromosome += str(self.liqueur_amts)
        chromosome += '\nmodifier_types: '
        chromosome += str(self.modifier_types)
        chromosome += '\nmodifier amts: '
        chromosome += str(self.modifier_amts)
        chromosome += '\nmixer_types: '
        chromosome += str(self.mixer_types)
        chromosome += '\nmixer_amts: '
        chromosome += str(self.mixer_amts)
        chromosome += '\n}\n'
        return chromosome

    def recipe(self):
        chromosome = self.name
        chromosome += '\n'
        for alc in range(len(self.alcohol_types)):
            chromosome += str(self.alcohol_amts[alc]) + ' ' + self.alcohol_types[alc] + '\n'
        for mix in range(len(self.mixer_types)):
            chromosome += str(self.mixer_amts[mix]) + ' ' + self.mixer_types[mix] + '\n'
        for mod in range(len(self.modifier_types)):
            chromosome += str(self.modifier_amts[mod]) + ' ' + self.modifier_types[mod] + '\n'
        return chromosome