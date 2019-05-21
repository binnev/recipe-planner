def parse_ingredient(ingredient):
    
    """ function to parse one ingredient line from a recipe file, based on 
    how many commas there are in the line (options listed below) """
    
    ing = ingredient.strip()  # strip whitespace
    if "," not in ing:  # if it's a single thing e.g. "butter"
        return None, None, ing
    elif ing.count(",") == 1:  # numbered without units e.g ."1, egg"
        n, thing = map(str.strip, ing.split(","))
        return float(n), None, thing
    elif ing.count(",") == 2:  # numberd with units e.g. 200, grams, flour
        n, unit, thing = map(str.strip, ing.split(","))
        """ I could add another function here to go and fetch the correct unit
        when multiple exist e.g. "gram, grams, g" --> fetch the correct one 
        from a list of aliases """
        return float(n), unit, thing
    else:
        raise Exception("too many commas in this ingredient line: "+ing)


def load_recipe(file):
    """ function to load a recipe from its .txt file and parse the lines into
    an organised dictionary """
    
    # open the file
    with open(file) as f:
        text = f.read().lower().split("\n")
        
    recipe = dict()
    
    # parse the recipe text and put the sections into a dict
    for ii, line in enumerate(text):
        if "=" in line:  # for lines defining properties of the recipe
            k, v = map(str.strip, line.split("="))
            recipe[k] = v
            
        if ":" in line:  # for lines defining sections
            # take the part before the ":" as the section label
            k = line.split(":")[0]
            
            # read until the next blank line or end of file
            things = []
            gen = (t for t in text[ii+1:])  # rest of the text after this line
            while True:  # keep reading lines until told to stop
                try:
                    item = next(gen)        # get the next line
                    if item == "":          # if the line is blank
                        break               # stop reading more lines
                    things.append(item)     # if line not blank, add item to list
                except StopIteration:       # if you reach the end of the file
                    break                   # stop reading more lines
            recipe[k] = things
                
    # parse the list of ingredients and rearrange into a dict
    ingredients = recipe["ingredients"]
    recipe["ingredients"] = d = dict()
    for ing in ingredients:
        n, u, t = parse_ingredient(ing)            
        d[t] = dict(units=u, amount=n)
        
    return recipe


def add_ingredients(ing1, ing2): 
    """ function to add together two of the same ingredient, with different 
    amounts and units """
    
            
        
def make_shopping_list(recipe_list):
    
    INGREDIENTS = dict()  # store the shopping list here
    EQUIPMENT = set()
    
    for ii, recipe in enumerate(recipe_list):
        ingredients = recipe["ingredients"]
        equipment = recipe.get("equipment")
        
        # for each ingredient, add it to the shopping list
        for ing, v in ingredients.items():  
            units, amount = v["units"], v["amount"]
            
            # if it isn't already in the shopping list
            if ing not in INGREDIENTS:
                # add it to the shopping list
                INGREDIENTS[ing] = {units: amount}
                
            else:  # if the ingredient is already in the list
                # attempt to merge it with the existing one
                
                # if no amount was given for this ingredient, skip this ingr.
                if amount is None:
                    continue
                
                # if an amount is given, add it to the existing unit amount
                if units not in INGREDIENTS[ing]:  # if there's no entry for this unit
                    INGREDIENTS[ing][units] = amount  # make a new entry
                else:  # if there's already an entry for this unit 
                    INGREDIENTS[ing][units] += amount  # add the amount
                    
        # make equipment list
        if equipment is not None:
            for eq in equipment:
                EQUIPMENT.add(eq)
                    
    return INGREDIENTS, EQUIPMENT


def print_shopping_list(INGREDIENTS):
    print("SHOPPING LIST:")
    for ing, v in INGREDIENTS.items():  # for each entry
        for unit, amount in v.items():
            # convert to strings and remove Nones
            if amount is None:
                amount = ""
            else:
                if amount % 1 == 0:  # remove decimal place from integer amounts
                    amount = int(amount)
                amount = str(amount)+" "
            unit = "" if unit is None else str(unit)+" "
            print(amount+unit+ing)
    
# main part of the program here
import glob

recipe_files = glob.glob("recipes/*.txt")
recipes = [load_recipe(file) for file in recipe_files]
#recipes = []
#for file in recipe_files:
#    recipes.append(load_recipe(file))
INGREDIENTS, EQUIPMENT = make_shopping_list(recipes)
print_shopping_list(INGREDIENTS)

"""
TODO:
- write a recipe class?
- write a search function
- write the main program that guides the user--executable in the python command 
    line 
"""
