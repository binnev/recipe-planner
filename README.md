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
To preserve the natural-language feel of the input files, I have implemented a simple syntax for the ingredients. Commas separate the amount, units, and name of the ingredient. 

Not all ingredients require all three fields, so the user can leave some out. Three modes are supported:
```yaml
ingredients:
  # amount, units, name
  - 1, tsp, chilli powder # 2 commas = all three fields
  - 2, large white onions # 1 comma = no units
  - fresh coriander       # no comma = only name
```

Writing this with correct YAML syntax produces overly cumbersome input files: 
```yaml
ingredients:
  - chilli powder:
    amount: 1
    units: tsp
  - large white onions: 
    amount: 2
    units: None
  - fresh coriander
    amount: None
    units: None    
```

## Aims: 
- Store recipes electronically
- Plan meals: generate a single shopping list for multiple recipes
- Use up spare pantry items: find recipes that best match user-provided spare pantry items
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTcxMjg0MDE3Nl19
-->