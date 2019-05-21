import glob
from functions import *

recipe_files = glob.glob("recipes/*.txt")
recipes = []
for file in recipe_files:
    recipes.append(load_recipe(file))
INGREDIENTS, EQUIPMENT = make_shopping_list(recipes)
print_shopping_list(INGREDIENTS)