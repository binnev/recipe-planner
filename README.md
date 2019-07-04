# recipe-planner
A recipe database and Python-based piece of software to organise recipes and plan shopping lists. 

## Cooking the recipes
Go to the [`readable-recipes folder`](https://github.com/binnev/recipe-planner/tree/master/readable-recipes). Click on one of the `.md` files to view it. These should render nicely on phones, tablets, etc. 

## YAML Recipe format
The input files are `YAML` format in the `recipes` folder. There are 3 required fields in the `YAML` files: 
- title (string)
- ingredients (list; see below for formatting rules)
- method (list)

The "author" and "source" fields will produce lines in the output markdown files. 

The user can add other fields provided they have correct `YAML` syntax, but the python script won't currently do anything with them.

## Aims: 
- Store recipes electronically
- Plan meals: generate a single shopping list for multiple recipes
- Use up spare pantry items: find recipes that best match user-provided spare pantry items
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA1MzA0MTk4M119
-->