### To play around with changing the training scores:

Look through ```convertedTrainingRecipes.txt``` to see the recipes for the drinks.  
Change the score for the corresponding drink in ```Sheet 1-Training Input Scores.csv```  
When you're done, grab just the scores and put them in ```train_out.txt``` (one per line, how it copy/pastes).  

### To change the sub-categories within the ingredient types:

Take a look at the pre-existing types in ```Sheet 2-Ingredient Types and Sub-Categories.csv```  
If you want to create a new one, or change where certain ingredients are, change the type in ```normalIngredients.txt```  
If you add a new type, add a case for it in the function ```train_input_setup()``` in ```geneticalgorithm.py``` (you'll have to add a new element to the corresponding category list (alcohol, modifier, mixer), and a case handling it and putting it in the correct index of the list.   

### To see if the algorithm started doing any better...
```
python3 geneticalgorithm.py 
```
