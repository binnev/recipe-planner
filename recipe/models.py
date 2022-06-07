from django.db import models

from recipe.aliases import INGREDIENT_ALIASES


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author, null=True, blank=True, related_name="recipes", on_delete=models.CASCADE
    )
    prep_time = models.IntegerField(null=True, blank=True)
    cook_time = models.IntegerField(null=True, blank=True)
    serves = models.CharField(null=True, blank=True, max_length=10)
    source = models.CharField(null=True, blank=True, max_length=200)
    image = models.CharField(null=True, blank=True, max_length=100)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.author}"


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=15, null=True, blank=True)
    description = models.CharField(max_length=50)
    preparation = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        s = f"{self.proper_name}"
        if self.unit:
            s = f"{self.unit} of {s}"
        if self.amount:
            amount = int(self.amount) if self.amount % 1 == 0 else self.amount
            s = f"{amount} {s}"
        if self.preparation:
            s = f"{s}, {self.preparation}"
        return s

    @property
    def proper_name(self):
        return INGREDIENT_ALIASES.get(self.description, self.description)


class Equipment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="equipment", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MethodStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="method_steps", on_delete=models.CASCADE)
    description = models.TextField()
