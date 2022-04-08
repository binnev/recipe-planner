from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name="recipes", on_delete=models.CASCADE)
    prep_time = models.IntegerField(null=True)
    cook_time = models.IntegerField(null=True)
    serves = models.CharField(null=True, blank=True, max_length=10)
    source = models.CharField(null=True, blank=True, max_length=100)
    image = models.CharField(null=True, blank=True, max_length=100)
    notes = models.TextField()


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="ingredients", on_delete=models.CASCADE)
    amount = models.FloatField()
    unit = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    preparation = models.CharField(max_length=50)


class Equipment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="equipment", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
