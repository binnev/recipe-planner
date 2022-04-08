from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, null=True, related_name="recipes", on_delete=models.CASCADE)
    prep_time = models.IntegerField(null=True)
    cook_time = models.IntegerField(null=True)
    serves = models.CharField(null=True, blank=True, max_length=10)
    source = models.CharField(null=True, blank=True, max_length=200)
    image = models.CharField(null=True, blank=True, max_length=100)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.author}"


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    amount = models.FloatField(null=True)
    unit = models.CharField(max_length=15, null=True, blank=True)
    description = models.CharField(max_length=50)
    preparation = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.amount} {self.unit} of {self.description}"


class Equipment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="equipment", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MethodStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="method_steps", on_delete=models.CASCADE)
    description = models.TextField()
