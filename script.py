#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 19:10:03 2019

@author: rmn
"""

import glob

recipe_files = glob.glob("recipes/*.txt")
recipes = []
for file in recipe_files:
    recipes.append(load_recipe(file))
INGREDIENTS, EQUIPMENT = make_shopping_list(recipes)
print_shopping_list(INGREDIENTS)