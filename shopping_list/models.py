from django.db import models

from recipe.exceptions import FailedConversion
from utils.in_memory_queryset import InMemoryQuerySet


class ShoppingList(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def aggregated_items(self):
        items = InMemoryQuerySet()
        for planned_recipe in self.recipes.iterator():
            for ingredient in planned_recipe.recipe.ingredients.iterator():
                if ingredient.amount:
                    ingredient.amount *= planned_recipe.scale_by

                # matching name and units --> just add the amount
                if existing := items.filter(
                    proper_name=ingredient.proper_name,
                    proper_unit=ingredient.proper_unit,
                ).first():
                    existing.amount += ingredient.amount

                # matching name, different units --> attempt to convert units
                elif existing := items.filter(proper_name=ingredient.proper_name).first():
                    try:
                        existing.amount += ingredient.amount_in_units(existing.proper_unit)
                    except FailedConversion:
                        items.append(ingredient)

                # nothing matching yet
                else:
                    items.append(ingredient)
        items = list(sorted(items, key=lambda ing: ing.proper_name))
        return "\n".join(map(str, items))


class PlannedRecipe(models.Model):
    shopping_list = models.ForeignKey(
        ShoppingList, related_name="recipes", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey("recipe.Recipe", on_delete=models.CASCADE)
    scale_by = models.IntegerField(default=1)
