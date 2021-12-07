class Chromosome():

    def __init__(self, liquor_types, liquor_amts, modifier_types, modifier_amts, mixer_types, mixer_amts):
        self.liquor_types = liquor_types
        self.liquor_amts = liquor_amts
        self.modifier_types = modifier_types
        self.modifier_amts = modifier_amts
        self.mixer_types = mixer_types
        self.mixer_amts = mixer_amts
        self.attributes = [liquor_types, liquor_amts, modifier_types, modifier_amts, mixer_types, mixer_amts]

    def __init__(self):
        self.liquor_types = []
        self.liquor_amts = []
        self.modifier_types = []
        self.modifier_amts = []
        self.mixer_types = []
        self.mixer_amts = []
        self.attributes = [liquor_types, liquor_amts, modifier_types, modifier_amts, mixer_types, mixer_amts]

    def set_from_attributes(self):
        self.liquor_types = self.attributes[0]
        self.liquor_amts = self.attributes[1]
        self.modifier_types = self.attributes[2]
        self.modifier_amts = self.attributes[3]
        self.mixer_types = self.attributes[4]
        self.mixer_amts = self.attributes[5]