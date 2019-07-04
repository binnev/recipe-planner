import yaml
import glob
import pathlib
import string

def parse_ingredient(ingredient):
    """ function to parse one ingredient line from a recipe file, based on
    how many commas there are in the line (options listed below).

    Returns (amount, units, ingredient)"""

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
    """ function to load a recipe from a YAML file. Requires the PyYAML library """
    # open the file
    file = pathlib.Path(file)
    with open(file) as f:
        recipe = yaml.safe_load(f)

    # check required fields
    required_fields = "title", "ingredients", "method"
    for field in required_fields:
        if field not in recipe:
            raise Exception("Recipe {} does not contain "
                            "required field '{}'".format(file, field))

    # add source directory to recipe
    recipe["source_dir"] = file.parent if file.parent else pathlib.Path()

    # if there's an image entry, prepend source dir to image path
    if "image" in recipe:
        img = pathlib.Path(recipe["image"])
        recipe["image"] = recipe["source_dir"] / img

    # parse ingredient lines
    ingredients = recipe["ingredients"]
    recipe["ingredients"] = d = dict()
    for ing in ingredients:
        amount, units, ingredient = parse_ingredient(ing)
        # remove decimal from integer amounts (e.g. 2.0 apples)
        if amount and (amount % 1 == 0):
            amount = int(amount)
        d[ingredient] = dict(units=units, amount=amount)

    return recipe


def punctuation_to_dashes(s):
    return "".join(map(lambda x: "-" if x in string.punctuation else x, s))


def recipe_to_markdown(recipe, filename=None, directory=None):
    """ store a recipe in an easily readable markdown format (good for phones in the
    kitchen) """

    # create a filename if none is given
    if filename is None:
        # remove punctutation
        """TODO: this is not very efficient. Replace with a regex"""
#        filename = "".join(c for c in recipe["title"] if c not in string.punctuation)

        filename = punctuation_to_dashes(recipe["title"])
        filename = filename.strip()
        # convert spaces to dashes
        filename = filename.replace(" ", "-")+".md"
        pathlib.Path(filename)

    # append markdown file extension if not included already
    if ".md" not in filename:
        filename = filename.with_suffix(".md")

    # prepend the directory to the filename if directory is passed
    if directory:
        directory = pathlib.Path(directory)
        filename = directory / filename

        # also create relative path to image
        if "image" in recipe:
            relative_path_to_cwd = pathlib.Path("/".join(".." for i in directory.parts))
            recipe["image"] = relative_path_to_cwd / recipe["image"]

    # construct list of lines to write to file
    lines = ["# {}\n".format(recipe["title"].title())]  # write title
    # optional entries
    if "author" in recipe:
        lines.append("Author: {}\n".format(recipe["author"]))
    if "source" in recipe:
        lines.append("From {}\n".format(recipe["source"]))
    if "image" in recipe:
        lines.append("<img src='{}' width='300px'>\n".format(recipe["image"]))
    # write ingredients list
    lines.append("\n## Ingredients:\n")
    for ingredient, values in recipe["ingredients"].items():
        units, amount = values["units"], values["amount"]
        line = [amount, units, ingredient]  # assemble ingredient line
        line = filter(None, line)           # remove None and other False values
        line = " ".join(map(str, line))     # convert to strings
        lines.append("- [ ] {}\n".format(line))
    # write method
    lines.append("\n## Method:\n")
    for ii, step in enumerate(recipe["method"]):
        lines.append("{}. {}\n".format(ii+1, step))

    # write lines to file
    with open(filename, mode="w") as f:
        f.writelines(lines)

    return None


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

# %% TODO
"""
- [ ] write a recipe class?
- [ ] write a search function
- [ ] write the main program that guides the user--executable in the python command
    line
- [x] fix broken images---use relative paths
"""

# %% testing
if __name__ == "__main__":
    recipe_files = glob.glob("recipes/*.yaml")
    for file in recipe_files:
        recipe = load_recipe(file)
        recipe_to_markdown(recipe, directory="readable-recipes")

    '''
    recipe_files = glob.glob("recipes/*.txt")
    recipes = [load_recipe(file) for file in recipe_files]
    INGREDIENTS, EQUIPMENT = make_shopping_list(recipes)
    print_shopping_list(INGREDIENTS)
    #'''
