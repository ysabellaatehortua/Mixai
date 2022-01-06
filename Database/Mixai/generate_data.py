import os
import django
from importDrinks import *
from Mixai.wsgi import *
from catalog.models import Cocktails, Ingredients, RecipeSteps, Measurements

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mixai.settings')
django.setup()

Alcohols = ("Dark rum", "Light rum", "Vodka", "Absolut Kurant", "Malibu rum", "Lager", "Tequila", "Wild Turkey", "Goldschlager", "J\u00e4germeister", "Jack Daniels", "Johnnie Walker", "Jim Beam", "Gin", "Peach Vodka", "Vanilla vodka", "Absolut Citron", "Absolut Vodka", "Applejack", "Vermouth",  "Scotch", "Sweet Vermouth", "Dry Vermouth", "Blended whiskey", "Bourbon", "Blackberry brandy", "Champagne", "Rye Whiskey", "Rum", "Bacardi Limon", "151 proof rum", "Sloe gin", "Southern Comfort", "Cachaca", "Cherry brandy", "Spiced rum", "A\u00f1ejo rum", "blackstrap rum", "Port", "Brandy", "White rum", "Lillet Blanc", "Grain alcohol", "Pisco", "Whiskey", "Dubonnet Rouge", "Absinthe", "Apricot brandy", "Mezcal", "Firewater", "Absolut Peppar", "Cognac", "Beer", "Irish whiskey", "Peach brandy", "Anis", "Apple brandy", "Tennessee whiskey", "Cranberry vodka", "Red wine", "Blended Scotch", "Islay single malt Scotch", "Everclear", "Prosecco", "Coffee brandy", "Lime vodka", "Crown Royal", "Raspberry vodka", "Ricard", "Ruby Port", "Irish Whiskey", "Rosso Vermouth", "White Wine", "Apple Brandy", "Surge", "Gold rum", "Pernod", "Ouzo", "Zima")

Mixers = ("Orange juice", "Cranberry juice", "Pineapple juice", "Milk", "Vanilla ice-cream", "Coca-Cola", "7-Up", "Cranberry Juice", "Tonic water", "Grapefruit juice", "Apple juice", "Peach nectar", "Passion fruit juice", "Hot Chocolate", "Tomato juice", "Water", "Cider", "Ginger ale", "Ginger Beer", "Soda water", "Coffee", "Pomegranate juice", "Fruit juice", "Dr. Pepper", "Carbonated water", "Club soda", "Lemonade", "Iced tea", "Schweppes Russchian", "Pepsi Cola", "Tea", "Grape Soda", "Coconut milk", "Pink lemonade", "Lemon-lime soda", "Tonic Water", "Orange Juice", "Limeade", "Root beer")

Modifiers = ("Lemon juice", "Roses sweetened lime juice", "Heavy cream", "Lime juice", "Sugar", "Light cream", "Sugar syrup", "Sour mix", "Worcestershire sauce", "Powdered sugar", "Vanilla extract", "Chocolate", "demerara Sugar", "Chocolate syrup", "Salt", "Whipping cream", "Vanilla syrup", "Espresso", "Egg", "Rose", "Strawberries", "Honey", "Apricot Nectar", "Pineapple Syrup", "Yoghurt", "Lemon peel", "Grapefruit Juice", "Sweet and sour", "Maraschino Cherry", "Corn syrup", "Butter", "Half-and-half", "Brown sugar", "Whipped cream", "Aperol", "Lemon", "Orgeat syrup", "Cocoa powder", "Rosemary Syrup", "Honey syrup", "Ginger Syrup", "Pineapple", "Passion fruit syrup", "Fresh Lime Juice", "Lime", "Raspberry syrup", "Blood Orange", "Allspice", "Apple", "Coriander", "Cream", "Maple syrup", "Agave Syrup", "Ice", "Cream of coconut", "Fruit")

Liqueurs = ("Grand Marnier", "Chambord raspberry liqueur", "Midori melon liqueur", "Amaretto", "Dark Creme de Cacao", "Cointreau", "Coconut liqueur", "Rumple Minze", "Triple sec", "Orange Curacao", "Grenadine", "Strawberry schnapps", "Kahlua", "maraschino liqueur", "Baileys irish cream", "Creme de Banane", "Sambuca", "Green Chartreuse", "Irish cream", "Peach schnapps", "Creme de Mure", "Blue Curacao", "Galliano", "Cherry Heering", "Falernum", "Campari", "Chocolate liqueur", "St. Germain", "Hot Damn", "Elderflower cordial", "Coffee liqueur", "Creme de Cacao", "Benedictine", "Raspberry Liqueur", "Lillet", "Green Creme de Menthe", "Yellow Chartreuse", "Apfelkorn", "Drambuie", "Tia maria", "Coconut Liqueur", "Butterscotch schnapps", "White Creme de Menthe", "Passoa", "Cherry liqueur", "Black Sambuca", "Creme de Cassis", "Amaro Montenegro", "Advocaat", "Godiva liqueur", "Anisette", "Creme De Banane", "Melon Liqueur", "Peachtree schnapps")


importedCocktails, importedIngredients, importedMeasurements, importedRecipes = main()

for drink in importedCocktails:
    alcoholic = importedRecipes[drink][0]
    drinkToAdd = Cocktails(cocktail_name = drink, alcoholic = alcoholic)
    drinkToAdd.save()

for ingredient in importedIngredients:
    type = ""
    if ingredient in Alcohols:
        type = "alcohol"
    elif ingredient in Mixers:
        type = "mixer"
    elif ingredient in Modifiers:
        type = "modifier"
    elif ingredient in Liqueurs:
        type = "liqueur"
    ingredientToAdd = Ingredients(ingredient_name = ingredient, ingredient_type = type)
    ingredientToAdd.save()

for measurement in importedMeasurements:
    measurementToAdd = Measurements(num_ounces = measurement[0])  
    measurementToAdd.save()
        
for drink in importedCocktails:
    drinkIngredients = importedRecipes[drink][2]
    drinkMeasurements = importedRecipes[drink][3]
    drinkObj = Cocktails.objects.get(cocktail_name = drink)
    for i in range(len(drinkIngredients)):
        curIngredient = drinkIngredients[i]
        curMeasurement = drinkMeasurements[i]
        ingredientObj = Ingredients.objects.get(ingredient_name = curIngredient)
        measurementObj = Measurements.objects.get(num_ounces = curMeasurement[0])
        recipeStepToAdd = RecipeSteps(cocktail = drinkObj, ingredient = ingredientObj, measurement = measurementObj)
        recipeStepToAdd.save()



# # Create a new record using the model's constructor.
# record = MyModelName(my_field_name="Instance #1")

# # Save the object into the database.
# record.save()

# # Access model field values using Python attributes.
# print(record.id) # should return 1 for the first record.
# print(record.my_field_name) # should print 'Instance #1'

# # Change record by modifying the fields, then calling save().
# record.my_field_name = "New Instance Name"
# record.save()


# all_books = Book.objects.all()

# wild_books = Book.objects.filter(title__contains='wild')
# number_wild_books = wild_books.count()