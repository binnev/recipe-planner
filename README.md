# recipe-planner
A recipe database and Python-based piece of software to organise recipes and plan shopping lists. 

## Cooking the recipes
Go to the [`readable-recipes folder`](https://github.com/binnev/recipe-planner/tree/master/readable-recipes). Click on one of the `.md` files to view it. These should render nicely on phones, tablets, etc. 

## Recipe format
The input files are `YAML` format in the `recipes` folder. There are ? required fields in the `YAML` files: 
- title (string)
- ingredients (list; see below for formatting rules)
- method (list)

## Aims: 
- Store recipes electronically
- Plan meals: generate a single shopping list for multiple recipes
- Use up spare pantry items: find recipes that best match user-provided spare pantry items
