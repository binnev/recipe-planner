from django.db import models

from utils.in_memory_queryset import InMemoryQuerySet


class ShoppingList(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def aggregated_items(self):
        items = InMemoryQuerySet()
        for planned_recipe in self.recipes.iterator():
            for ing in planned_recipe.recipe.ingredients.iterator():
                if ing.amount:
                    ing.amount *= planned_recipe.scale_by
                if matching_ing := items.filter(proper_name=ing.proper_name, unit=ing.unit).first():
                    matching_ing.amount = (matching_ing.amount or 0) + (ing.amount or 0)
                else:
                    items.append(ing)
        items = list(sorted(items, key=lambda ing: ing.description))
        return "\n".join(map(str, items))


class PlannedRecipe(models.Model):
    shopping_list = models.ForeignKey(
        ShoppingList, related_name="recipes", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey("recipe.Recipe", on_delete=models.CASCADE)
    scale_by = models.IntegerField(default=1)
