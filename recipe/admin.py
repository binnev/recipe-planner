from django.contrib import admin

from recipe.models import Recipe, Ingredient, Equipment, MethodStep


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0
    fields = (
        "amount", "unit", "description", "preparation"
    )


class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 0
    fields = ("name",)


class MethodStepInline(admin.TabularInline):
    model = MethodStep
    extra = 0
    fields = ("description",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "author",
        "prep_time",
        "cook_time",
        "serves", "source", "image", "notes"
    )
    inlines = (
        IngredientInline, EquipmentInline, MethodStepInline,
    )
