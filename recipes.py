import yaml
import glob
import pathlib
import string

def parse_ingredient(ingredient_line):
    """ function to parse one ingredient line from a recipe file, based on
    how many commas there are in the line (options listed below).

    Returns (amount, units, ingredient)"""

    amount, units, ingredient, prep = None, None, None, None
    ingredient_line = ingredient_line.strip()  # strip whitespace
    if "," not in ingredient_line:  # if it's a single thing e.g. "butter"
        ingredient = ingredient_line
    elif ingredient_line.count(",") == 1:  # numbered without units e.g ."1, egg"
        amount, ingredient = map(str.strip, ingredient_line.split(","))
    elif ingredient_line.count(",") == 2:  # numberd with units e.g. 200, grams, flour
        amount, units, ingredient = map(str.strip, ingredient_line.split(","))
    else:
        raise Exception("too many commas in this ingredient line: "+ingredient_line)

    # convert amount to numeric if present
    if amount:
        amount = float(amount)
        # and remove decimal point for integer amounts
        if amount % 1 == 0:
            amount = int(amount)

    # split off preparation instructions if present
    if ";" in ingredient:
        ingredient, prep = map(str.strip, ingredient.split(";"))

    return amount, units, ingredient, prep

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
        amount, units, ingredient, prep = parse_ingredient(ing)
        d[ingredient] = dict(units=units, amount=amount, prep=prep)

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

        # also create relative path to image, if image passed
        if "image" in recipe:
            relative_path_to_cwd = pathlib.Path("/".join(".." for i in directory.parts))
            recipe["image"] = relative_path_to_cwd / recipe["image"]

    # construct list of lines to write to file
    lines = ["# {}\n".format(recipe["title"].capitalize())]  # write title
    # optional entries
    if "author" in recipe:
        lines.append("Author: {}\n\n".format(recipe["author"].title()))
    if "source" in recipe:
        lines.append("From {}\n\n".format(recipe["source"]))
    if "image" in recipe:
        lines.append("<img src='{}' width='300px'>\n\n".format(recipe["image"]))
    # write ingredients list
    lines.append("\n## Ingredients:\n")
    for ingredient, values in recipe["ingredients"].items():
        units, amount, prep = values["units"], values["amount"], values["prep"]
        line = [amount, units, ingredient]  # assemble ingredient line
        line = filter(None, line)           # remove None and other False values
        line = " ".join(map(str, line))     # convert to strings
        if prep:                            # add preparation instructions if present
            line += ", "+prep
        lines.append("- [ ] {}\n".format(line))
    # write method
    lines.append("\n## Method:\n")
    for ii, step in enumerate(recipe["method"]):
        step = step.strip()
        step = step[0].capitalize()+step[1:]  # capitalise first letter
        if step[-1] != ".":
            step = step+"."
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
- [ ] add support for multiple ingredients lists. E.g. one for fishball mix, and one
    for the curry mix. (a) subdivide ingredients list using dicts? Then the load
    function and the md save function will have to be able to parse this. (b) Have
    multiple ingredients lists: "ingredients-fish ball mix: ...list..." and
    "ingredients-curry mix: ...list...". Then have the load/save functions do their
    ingredients routine on ANY property of the recipe that *contains* the word
    "ingredients".
- [x] have another field in each ingredient for "prep". This will contain the stuff
    after the semicolon in "2, large white onions; finely chopped". This will prevent
    preparation instructions clashing with other entries of the same ingredient from
    other recipes.
- [ ] Add another function to go and fetch the correct unit when multiple exist e.g.
    "gram, grams, g" --> fetch the correct one from a list of aliases

"""

# %% testing
if __name__ == "__main__":
    recipe_files = glob.glob("recipes/*.yaml")
    recipes = [load_recipe(file) for file in recipe_files]

    for recipe in recipes:
        recipe_to_markdown(recipe, directory="readable-recipes")

    ''

    INGREDIENTS, EQUIPMENT = make_shopping_list(recipes)
    print_shopping_list(INGREDIENTS)
    #'''
