
import glob


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


def load_recipe(text):
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


recipe_files = glob.glob("*.txt")
recipes = []
for file in recipe_files:
    recipes.append(load_recipe(file))
            
        
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
                if units not in INGREDIENTS[ing]:  # if there's no entry for this unit
                    INGREDIENTS[ing][units] = amount  # make a new entry
                else:  # if there's already an entry for this unit 
                    try:
                        INGREDIENTS[ing][units] += amount  # add the amount
                        """ probably need to add a try/except here to catch Nones """
                    except TypeError:
                        print("i did a dookie. Sorry.")
                    finally:
                        print("For ingredient {} I was trying to add {} to {}".format(ing, amount, units))
                    
        # make equipment list
        if equipment is not None:
            for eq in equipment:
                EQUIPMENT.add(eq)
                    
    return INGREDIENTS, EQUIPMENT
    

INGREDIENTS, EQUIPMENT = make_shopping_list(recipes)

def print_shopping_list(INGREDIENTS):
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
    
    
    
    
    
    
    
    
    
    
print_shopping_list(INGREDIENTS)