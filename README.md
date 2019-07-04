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

### Ingredient syntax
To preserve the natural-language feel of the input files, I have implemented a simple syntax for the ingredients. Commas separate the amount, units, and name of the ingredient: 
```
- 1, tsp, chilli powder
```

Following the YAML syntax seems overly cumbersome. Instead of defining an ingredient like this: 
```yaml
- potatoes:
    amount: 1
    units: kg
    prep: chopped into cubes
```
we can instead write: 
```yaml
- 1, kg, potatoes; chopped into cubes
```

```yaml
ingredients:
  - 1, tsp, chilli powder
  - 2, large white onions
  - fresh coriander
```

## Aims: 
- Store recipes electronically
- Plan meals: generate a single shopping list for multiple recipes
- Use up spare pantry items: find recipes that best match user-provided spare pantry items
<!--stackedit_data:
eyJoaXN0b3J5IjpbNDc1NDAwMTcyXX0=
-->