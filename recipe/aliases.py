_INGREDIENT_ALIASES = {
    "ground cumin": ["cumin powder"],
    "ground coriander": ["coriander powder"],
    "hot chilli powder": ["chilli powder"],
    "ground turmeric": ["turmeric", "turmeric powder"],
    "white onion": ["large white onion", "medium onions", "onions", "onion"],
}

KG = "kg"
G = "g"
TBSP = "tbsp"
TSP = "tsp"
ML = "ml"
L = "l"

_UNIT_ALIASES = {
    KG: ["kilo", "kilos", "kilograms", "kgs"],
    G: ["gr", "gram", "grams", "gs"],
    TBSP: ["tbsps", "tablespoon", "tablespoons"],
    TSP: ["tsps", "teaspoon", "teaspoons"],
    ML: ["millilitres", "millilitre", "milliliters", "milliliter"],
    L: ["litres", "litre", "liters", "liter"],
    "clove": ["cloves"],  # of garlic
}

_UNIT_RATIOS = {
    KG: {1000: G},
    L: {1000: ML},
    TBSP: {3: TSP},
}

INGREDIENT_ALIASES = {
    alias: preferred_name
    for preferred_name, aliases in _INGREDIENT_ALIASES.items()
    for alias in aliases
}

UNIT_ALIASES = {
    alias: preferred_name for preferred_name, aliases in _UNIT_ALIASES.items() for alias in aliases
}

UNIT_RATIOS = {
    unit: {v: k for k, v in related_units.items()} for unit, related_units in _UNIT_RATIOS.items()
}
