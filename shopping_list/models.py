from django.db import models

class ShoppingList(models.Model):
    recipes = models.ManyToManyField("recipe.Recipe")
    date_created = models.DateTimeField(auto_now_add=True)