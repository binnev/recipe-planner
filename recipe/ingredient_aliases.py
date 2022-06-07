_PREFERRED_NAME_TO_ALIASES = {
    "ground cumin": ["cumin powder"],
    "ground coriander": ["coriander powder"],
    "hot chilli powder": ["chilli powder"],
    "turmeric powder": ["turmeric"],
    "white onion": ["large white onion", "medium onions", "onions", "onion"],
}

INGREDIENT_ALIASES = {
    alias: preferred_name
    for preferred_name, aliases in _PREFERRED_NAME_TO_ALIASES.items()
    for alias in aliases
}
